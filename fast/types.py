from enum import Enum
from typing import NewType

TaskId = NewType("TaskId", int)


class TaskState(str, Enum):
    open = "open"
    processing = "processing"
    closed = "closed"
