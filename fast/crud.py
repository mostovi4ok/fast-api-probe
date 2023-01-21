from collections.abc import Sequence

from fastapi import BackgroundTasks
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .celery_app import close_task
from .errors import InValidTaskState, NotTask
from .models import Task
from .shemas import NewTask
from .types import TaskId, TaskState


async def all_open_tasks(session: AsyncSession) -> Sequence[Task]:
    query = select(Task).filter_by(state=TaskState.open).order_by(Task.id)
    return (await session.scalars(query)).all()


async def create_task(session: AsyncSession, task_params: NewTask) -> Task:
    task = Task(name=task_params.name, state=TaskState.open)
    session.add(task)
    return task


async def modify_task_state(session: AsyncSession, task_id: TaskId, background_tasks: BackgroundTasks) -> Task:
    query = select(Task).where(Task.id == task_id)
    if (task := await session.scalar(query)) is None:
        raise NotTask(task_id)

    if task.state != TaskState.open:
        raise InValidTaskState(task.id)

    task.state = TaskState.processing
    background_tasks.add_task(close_task.delay, task_id)
    return task
