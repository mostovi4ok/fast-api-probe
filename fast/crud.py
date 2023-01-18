from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .celery_app import close_task
from .models import Task
from .shemas import NewTask
from .types import TaskId, TaskState
from .errors import NotTask, InValidTaskState


async def all_open_tasks(session: AsyncSession) -> Sequence[Task]:
    query = select(Task).filter_by(state=TaskState.open).order_by(Task.id)
    return (await session.scalars(query)).all()


async def create_task(session: AsyncSession, task_params: NewTask) -> Task:
    async with session.begin():
        task = Task(name=task_params.name, state=TaskState.open)
        session.add(task)

    return task


async def modify_task_state(session: AsyncSession, task_id: TaskId) -> Task:
    async with session.begin():
        query = select(Task).where(Task.id == task_id)
        if (task := await session.scalar(query)) is None:
            raise NotTask(task_id)

        if task.state != TaskState.open:
            raise InValidTaskState(task.id)

        task.state = TaskState.processing

    close_task.delay(task_id)
    return task
