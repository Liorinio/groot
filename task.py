from abc import ABC, abstractmethod
from typing import Any


class Task(ABC):
    """
        The Task's constructor. it receives a number which represents the id of the task, name for the task,
        a number which defines how many retries the task will have and a dictionary that contains exceptions
        and a boolean value which determines if the user wants to check this exception in its code or not
        """
    def __init__(self, task_id: int, max_retries: int, name: str, exceptions_retry: dict[Exception, bool]):
        self.task_id = task_id
        self.max_retries = max_retries
        self.name = name
        self.exceptions_retry = exceptions_retry # a dict that contains exceptions and if the user wants to use them or not

    # the function that the user overrides in order to implement his code
    @abstractmethod
    def action(self, user_input: Any|None):
        pass

    # gets an exception and runs the action again
    def retry(self, required_exception:Exception, is_on:bool):
        ...

    """
    The on_failure() function runs on the exceptions array, checks if the exception is in the exception dictionary and if the check value of it is true.
    if both of the conditions are met, it runs the retry function
    """
    def on_failure(self, required_exception:Exception):
        if required_exception in self.exceptions_retry.values() and self.exceptions_retry[required_exception]:
            self.retry(required_exception, True)