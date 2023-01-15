from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Task
from .shemas import NewTask
from .types import TaskState


async def all_open_tasks(session: AsyncSession) -> Sequence[Task]:
    query = select(Task).filter_by(state=TaskState.open).order_by(Task.id)
    return (await session.scalars(query)).all()


async def create_task(session: AsyncSession, task_params: NewTask) -> Task:
    async with session.begin():
        task = Task(name=task_params.name, state=TaskState.open)
        session.add(task)

    return task
