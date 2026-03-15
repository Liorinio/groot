import logging
import pandas as pd
from typing import Any, Callable
from basics.task import Task

logger = logging.getLogger(__name__)


def process(input_data: pd.DataFrame, columns: list[str]) -> pd.DataFrame | None:
    """
    The function receives a DataFrame and a list of columns to keep,
    and returns the DataFrame filtered to only those columns.
    """
    try:
        return input_data[columns]
    except Exception as e:
        logger.error(f"An error occurred during column filtering: {e}")
        return None


class FilterColumnsTask(Task):

    def __init__(self, task_id: str, name: str, columns: list[str],
                 max_retries: int = 3, exceptions_retry: dict[type, bool] | None = None):
        """
        The class's constructor. It receives the same parameters as its parent class
        in addition to a list of column names to keep in the DataFrame.
        """
        super().__init__(task_id=task_id, max_retries=max_retries, name=name,
                         exceptions_retry=exceptions_retry if exceptions_retry is not None else {})
        self.columns = columns

    def action(self, user_input: Any | None) -> pd.DataFrame | None:
        """
        The 'action()' function gets a DataFrame as user_input,
        validates the columns exist, and returns the filtered DataFrame.
        """
        self.__validate_columns(user_input)
        return process(user_input, self.columns)

    def on_failure(self) -> Callable:
        """
        The 'on_failure()' function returns __check_columns which guides
        the user when the filtering has failed.
        """
        return self.__check_columns

    def __validate_columns(self, df: pd.DataFrame):
        """
        A function that validates the DataFrame and checks that all requested
        columns exist in it.
        """
        if not isinstance(df, pd.DataFrame):
            self.is_task_failed = True
            logger.error("Error: user_input must be a pandas DataFrame.")
            return
        missing = [col for col in self.columns if col not in df.columns]
        if missing:
            self.is_task_failed = True
            logger.error(f"Error: The following columns were not found: {missing}")

    def __check_columns(self):
        """
        A function that checks if the requested columns exist in the data.
        If KeyError is already being retried, it prints a hint, otherwise enables retry.
        """
        if self.exceptions_retry.get(KeyError()):
            logger.warning("Check if the column names are correct and exist in your DataFrame.")
        else:
            self.exceptions_retry[KeyError()] = True