from pydantic import BaseModel, validator

from .types import TaskState


class NewTask(BaseModel):
    name: str

    @validator("name")
    def name_length(cls, n) -> str:
        if len(n) > 30:
            raise ValueError("too big")

        return n


class Task(BaseModel):
    id: int
    name: str
    state: TaskState

    class Config:
        orm_mode = True
