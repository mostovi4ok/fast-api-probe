from collections.abc import Sequence

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .errors import TaskError
from . import shemas
from . import crud
from .db import AsyncSessionFactory
from .models import Task


tasks_api = FastAPI()


@tasks_api.exception_handler(TaskError)
async def unicorn_exception_handler(request: Request, exc: TaskError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"message": exc.__class__.__name__},
    )


@tasks_api.get("/tasks/", response_model=Sequence[shemas.Task])
async def get_all_open_tasks() -> Sequence[Task]:
    async with AsyncSessionFactory() as session:
        return await crud.all_open_tasks(session)


@tasks_api.put("/tasks/", response_model=shemas.Task)
async def create_task(task_params: shemas.NewTask) -> Task:
    async with AsyncSessionFactory() as session:
        return await crud.create_task(session, task_params)


@tasks_api.post("/tasks/", response_model=shemas.Task)
async def modify_task_state(task_id_param: shemas.ModifiedTask) -> Task:
    async with AsyncSessionFactory() as session:
        return await crud.modify_task_state(session, task_id_param.id)
