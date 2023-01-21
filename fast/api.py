from collections.abc import Sequence

from fastapi import BackgroundTasks, FastAPI, Request
from fastapi.responses import JSONResponse

from . import crud, shemas
from .db import AsyncSessionFactory
from .errors import TaskError
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
        async with session.begin():
            return await crud.create_task(session, task_params)


@tasks_api.post("/tasks/", response_model=shemas.Task)
async def modify_task_state(task_id_param: shemas.ModifiedTask, background_tasks: BackgroundTasks) -> Task:
    async with AsyncSessionFactory() as session:
        async with session.begin():
            return await crud.modify_task_state(session, task_id_param.id, background_tasks)
