from collections.abc import AsyncIterator, Iterator

import pytest
from fastapi import BackgroundTasks
from sqlalchemy import Connection
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.background import BackgroundTask

from fast import crud, db, db_shema
from fast.celery_app import close_task
from fast.models import Task
from fast.shemas import NewTask
from fast.types import TaskState

pytestmark = pytest.mark.anyio


@pytest.fixture(scope="session")
def connection() -> Connection:
    return db.engine.connect()


@pytest.fixture(scope="session")
def setup_database(connection) -> Iterator[None]:
    db_shema.create_all()
    yield
    db_shema.drop_all()


@pytest.fixture(scope="session")
async def async_db_session(setup_database: None) -> AsyncIterator[AsyncSession]:
    async with db.async_engine.connect() as async_connection:
        async with db.AsyncSessionFactory(bind=async_connection) as async_db_session:
            yield async_db_session


@pytest.fixture
async def async_db_transaction(async_db_session: AsyncSession) -> AsyncIterator[AsyncSession]:
    async with async_db_session.begin() as session_begin:
        yield async_db_session
        await session_begin.rollback()


@pytest.fixture
async def opened_10_tasks(async_db_transaction: AsyncSession) -> list[Task]:
    return await create_tasks(async_db_transaction)


@pytest.fixture
async def one_opened_task(async_db_transaction: AsyncSession) -> Task:
    return (await create_tasks(async_db_transaction, 1))[0]


async def test_some_asyncio_code(async_db_transaction: AsyncSession) -> None:
    task_params = NewTask(name="test_name")
    task = await crud.create_task(async_db_transaction, task_params)
    assert task.name == task_params.name


async def test_read_objects_emty_bd(async_db_transaction: AsyncSession) -> None:
    tasks = await crud.all_open_tasks(async_db_transaction)
    assert not tasks


async def test_check_len_of_returned_objects(opened_10_tasks: list[Task], async_db_transaction: AsyncSession) -> None:
    len_tasks = len(opened_10_tasks)
    tasks_from_db = await crud.all_open_tasks(async_db_transaction)
    assert len_tasks == len(tasks_from_db)


async def test_check_ordering(opened_10_tasks: list[Task], async_db_transaction: AsyncSession) -> None:
    tasks_from_db = await crud.all_open_tasks(async_db_transaction)
    id_tasks = sorted(t.id for t in opened_10_tasks)
    id_tasks_from_db = [t.id for t in tasks_from_db]
    assert id_tasks == id_tasks_from_db


async def test_only_open_tasks_was_returned(async_db_transaction: AsyncSession) -> None:
    for state in TaskState:
        await create_tasks(async_db_transaction, state=state)

    tasks_from_db = await crud.all_open_tasks(async_db_transaction)
    tasks_state_from_db = {t.state for t in tasks_from_db}
    assert {TaskState.open} == tasks_state_from_db


async def test_background_tasks_was_colled(async_db_transaction: AsyncSession, one_opened_task: Task):
    background_tasks = BackgroundTasks()
    await crud.modify_task_state(async_db_transaction, one_opened_task.id, background_tasks)
    assert len(background_tasks.tasks) == 1
    wrapper: BackgroundTask = background_tasks.tasks[0]
    assert wrapper.func == close_task.delay


async def create_tasks(
    async_db_transaction: AsyncSession, count: int = 10, state: TaskState = TaskState.open
) -> list[Task]:
    tasks = [Task(name=f"{i}", state=state) for i in range(count - 1, -1, -1)]
    async_db_transaction.add_all(tasks)
    await async_db_transaction.flush()
    return tasks
