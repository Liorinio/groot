from logging import exception
from typing import Any


class Task:
    def __init__(self, task_id:int, max_retries: int, name: str, exceptions_retry:dict[exception,bool]):
        self.task_id = task_id
        self.max_retries = max_retries
        self.name = name
        self.exceptions_retry = exceptions_retry

    def action(self, user_input: Any|None):
        pass

    def retry(self, required_exception:exception, is_on:bool):
        ...

    def on_failure(self):
        ...
