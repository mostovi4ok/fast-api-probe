from typing import NewType
from enum import Enum


TaskId = NewType("TaskId", int)


class TaskState(str, Enum):
    open = "open"
    processing = "processing"
    closed = "closed"
