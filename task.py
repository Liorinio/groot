from typing import Any


class Task:
    def __init__(self, task_id:int, max_retries: int, name: str, exceptions_retry:dict[Exception,bool]):
        self.task_id = task_id
        self.max_retries = max_retries
        self.name = name
        self.exceptions_retry = exceptions_retry # a dict that contains exceptions and if the user wants to use them or not

    # the function that the user overrides in order to implement his code
    def action(self, user_input: Any|None):
        pass

    # gets an exception and runs the action again
    def retry(self, required_exception:Exception, is_on:bool):
        ...

    # runs on the exceptions array, checks which exception is on and runs the retry function
    def on_failure(self):
        ...
