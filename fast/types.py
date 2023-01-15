from enum import Enum


class TaskState(str, Enum):
    open = "open"
    closed = "closed"
