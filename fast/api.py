from collections.abc import Sequence

from fastapi import FastAPI

from . import shemas
from . import crud
from .db import async_session
from .models import Task


tasks_api = FastAPI()


@tasks_api.get("/tasks/", response_model=Sequence[shemas.Task])
async def all_open_tasks() -> Sequence[Task]:
    async with async_session() as session:
        return await crud.all_open_tasks(session)


@tasks_api.post("/tasks/", response_model=shemas.Task)
async def create_task(task_params: shemas.NewTask) -> Task:
    async with async_session() as session:
        return await crud.create_task(session, task_params)
