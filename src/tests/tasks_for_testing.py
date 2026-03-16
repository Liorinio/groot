import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler
from src.basics.task import Task
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

            libraries = {"pandas": pd, "numpy": np, "LinearRegression": LinearRegression,
                         "train_test_split": train_test_split,
                         "StandardScaler": StandardScaler, "r2_score": r2_score,
                         "KNeighborsRegressor": KNeighborsRegressor}

            logger.info("ML libraries imported successfully")

            self.is_task_failed = False
            return libraries

        except Exception as e:
            self.is_task_failed = True
            raise e

    def on_failure(self) -> Callable:
        def check_imports():
            if ImportError in self.exceptions_retry.keys() and self.exceptions_retry[ImportError()]:
                logger.warning("Failed to import ML libraries. Make sure required packages are installed.")
                logger.warning("Try installing them with: pip install pandas numpy scikit-learn matplotlib seaborn")

        return check_imports


class CsvLoaderTask(Task):
    def action(self, user_input: Any | None = None):
        try:
            df = pd.read_csv(user_input)
            logger.info("The dataframe was loaded successfully")

            self.is_task_failed = False
            return df.head()

        except Exception as e:
            self.is_task_failed = True
            raise e

    def on_failure(self) -> Callable:
        def check_loading():
            if FileNotFoundError in self.exceptions_retry.keys() and self.exceptions_retry[ImportError()]:
                logger.warning("Check the path you enterd.")

        return check_loading


class ScatterPlotTask(Task):
    def action(self, df: pd.DataFrame | None = None):
        try:
            plt.figure(figsize=(10, 5))
            plt.scatter(df['Possession%'], df['Pass%'])
            plt.xlabel('Possession')
            plt.ylabel('Pass')
            plt.title('Possession VS Pass')

            self.is_task_failed = False
            plt.show()
        except Exception as e:
            self.is_task_failed = True
            raise e

    def on_failure(self) -> Callable:
        def check_showing_graph():
            if self.exceptions_retry.get(ValueError()):
                logger.warning("Check if the data of both angles are the same size and are arrays.")
            elif self.exceptions_retry.get(NameError()):
                logger.warning("Check if you spelled the names correctly")

        return check_showing_graph

class SplittingDataTask(Task):
    def action(self, df: pd.DataFrame | None = None):
        try:
            x_train, x_test, y_train, y_test = train_test_split(df.drop(columns = ['Rating']), df['Rating'], test_size=0.3,random_state=2)
            self.is_task_failed = False
            return x_train, x_test, y_train, y_test

        except Exception as e:
            self.is_task_failed = True
            raise e

    def on_failure(self) -> Callable:
        def check_splitting():
            if self.exceptions_retry.get(ValueError()):
                logger.warning("Check if your target in 1D and your features are 2D.")
            if self.exceptions_retry.get(TypeError()):
                logger.warning("Check if your target and features are in the type they should be")

        return check_splitting


class TrainingNodelTask(Task):
    def action(self, train_test: tuple | None = None):
        try:
            x_train = train_test[0]
            x_test = train_test[1]
            y_train = train_test[2]
            y_test = train_test[3]
            model = LinearRegression(fit_intercept=True, copy_X=True, n_jobs=None, positive=True).fit(x_train, y_train)  # אימון המודל
            y_predict = model.predict(x_test)
            result = [x_train, x_test, y_train, y_test, model, y_predict]
            return result

        except Exception as e:
            self.is_task_failed = True
            raise e

    def on_failure(self) -> Callable:
        def check_training():
            logger.warning("Something went wrong. Please check")
        return check_training


class PredictionTask(Task):
    def action(self, training_results: list | None = None):
        try:
            predict = r2_score(training_results[3], training_results[-1])
            return predict

        except Exception as e:
            self.is_task_failed = True
            raise e

    def on_failure(self) -> Callable:
        def check_predicting():
            logger.warning("Something went wrong. Please check")
        return check_predicting
