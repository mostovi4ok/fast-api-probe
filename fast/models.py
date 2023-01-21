from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from .types import TaskState


class Base(DeclarativeBase):
    pass


class Task(Base):

    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    state: Mapped[TaskState]
