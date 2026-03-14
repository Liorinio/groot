from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any


class Task(ABC):

    def __init__(self, task_id: str, max_retries: int, name: str, exceptions_retry: dict[Exception, bool]):
        """
        The Task's constructor. it receives a number which represents the id of the task, name for the task,
        a number which defines how many retries the task will have and a dictionary that contains exceptions
        and a boolean value which determines if the user wants to check this exception in its code or not
        """
        self.task_id = task_id
        self.max_retries = max_retries
        self.name = name
        self.exceptions_retry = exceptions_retry
        # a dict that contains exceptions and if the user wants to use them or not

    @abstractmethod
    def action(self, user_input: Any | None):
        """
        the function that the user overrides in order to implement his code
        """

    @abstractmethod
    def on_failure(self) -> Callable:
        """
        The on_failure() function is a function that the user overrides to create a function that defines what will
        happen when all the retries have failed
        """
        ...
