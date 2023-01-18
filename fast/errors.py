class TaskError(Exception):
    pass


class NotTask(TaskError):
    pass


class InValidTaskState(TaskError):
    pass
