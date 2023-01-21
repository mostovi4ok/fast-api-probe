from celery import Celery
from sqlalchemy import select

from . import env
from .db import SessionFactory
from .models import Task
from .types import TaskId, TaskState

app = Celery("tasks", broker=env.CELERY_BROKER)


@app.task
def close_task(task_id: TaskId) -> None:
    with SessionFactory.begin() as session:
        query = select(Task).where(Task.id == task_id)
        if (task := session.scalar(query)) is None:
            return

        if task.state == TaskState.processing:
            task.state = TaskState.closed
