from sklearn.preprocessing import StandardScaler
from basics.task import Task
import logging
from typing import Any, Callable


logger = logging.getLogger(__name__)


class ImportLibrariesTask(Task):
    def action(self, user_input: Any | None = None):
        try:
            import numpy as np
            import pandas as pd
            import matplotlib.pyplot as plt
            import seaborn as sns
            from sklearn.linear_model import LinearRegression
            from sklearn.model_selection import train_test_split
            from sklearn.metrics import r2_score
            from sklearn.neighbors import KNeighborsRegressor

            libraries = {
                "pandas": pd,
                "numpy": np,
                "LinearRegression": LinearRegression,
                "train_test_split": train_test_split,
                "StandardScaler": StandardScaler,
                "r2_score": r2_score,
                "KNeighborsRegressor": KNeighborsRegressor
            }

            print("ML libraries imported successfully")

            self.is_task_failed = False
            return libraries

        except Exception as e:
            self.is_task_failed = True
            raise e

    def on_failure(self) -> Callable:
        def handle_failure():
            if ImportError in self.exceptions_retry.keys() and self.exceptions_retry[ImportError()]:
                logger.warning("Failed to import ML libraries. Make sure required packages are installed.")
                logger.warning("Try installing them with: pip install pandas numpy scikit-learn matplotlib seaborn")

        return handle_failure