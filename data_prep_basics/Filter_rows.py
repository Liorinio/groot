import pandas as pd
from typing import Any, Callable

from basics.task import Task


def process(input_data: pd.DataFrame, condition: Callable[[pd.DataFrame], pd.Series]) -> pd.DataFrame | None:
    """
    The function receives a DataFrame and a condition function,
    and returns the DataFrame filtered to only the rows where the condition is True.
    """
    try:
        return input_data[condition(input_data)]
    except Exception as e:
        print(f"An error occurred during row filtering: {e}")
        return None


class FilterRowsTask(Task):

    def __init__(self, task_id: str, name: str, condition: Callable[[pd.DataFrame], pd.Series],
                 max_retries: int = 3, exceptions_retry: dict[type, bool] | None = None):
        """
        The class's constructor. It receives the same parameters as its parent class
        in addition to a condition function that determines which rows to keep.
        """
        super().__init__(task_id=task_id, max_retries=max_retries, name=name,
                         exceptions_retry=exceptions_retry if exceptions_retry is not None else {})
        self.condition = condition

    def action(self, user_input: Any | None) -> pd.DataFrame | None:
        """
        The 'action()' function gets a DataFrame as user_input,
        validates it, and returns the DataFrame filtered by the condition.
        """
        self.__validate_input(user_input)
        return process(user_input, self.condition)

    def on_failure(self) -> Callable:
        """
        The 'on_failure()' function returns __check_condition which guides
        the user when the row filtering has failed.
        """
        return self.__check_condition

    def __validate_input(self, df: pd.DataFrame):
        """
        A function that validates that user_input is a pandas DataFrame.
        """
        if not isinstance(df, pd.DataFrame):
            self.is_task_failed = True
            print("Error: user_input must be a pandas DataFrame.")

    def __check_condition(self):
        """
        A function that checks if the condition function is valid.
        If ValueError is already being retried, it prints a hint, otherwise enables retry.
        """
        if self.exceptions_retry.get(ValueError()):
            print("Check if your condition function returns a valid boolean Series.")
        else:
            self.exceptions_retry[ValueError()] = True