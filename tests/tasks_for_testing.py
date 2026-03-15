import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
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

            libraries = {"pandas": pd,"numpy": np,"LinearRegression": LinearRegression,"train_test_split": train_test_split,
                "StandardScaler": StandardScaler,"r2_score": r2_score,"KNeighborsRegressor": KNeighborsRegressor}

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