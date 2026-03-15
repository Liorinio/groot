import pickle
from typing import Callable, Any
from task import Task
from fastapi import FastAPI
from cli_commands_to_code import deploy_uvicorn


app = FastAPI()


def process(input_data,model):
    """
    The function receives input data from the user and the model that the user uses, and return the predictions of the model.
    """
    try:
        predictions = model.predict(input_data)
        return predictions

    except Exception as e:
        print(f"An error occurred during model loading or inference: {e}")
        return None


class DefaultModelTask(Task):

    def __init__(self,task_id: str,max_retries: int,name: str, exceptions_retry: dict[Exception, bool], model_path: str):
        super().__init__(task_id, max_retries, name, exceptions_retry)

        """
        The class's constructor. It receives the same parameters as its parent class in addition to a path to where the model is saved
        """

        self.model_path = model_path
        self.model = None

    def action(self, user_input: Any | None):
        """
        This function loads the model from the pickle file and returns its predictions.
        """
        self.__load_model()
        return process(user_input, self.model)

    def on_failure(self) -> Callable:
        """
        The 'on_failure()' function returns __check_storage which guides
        the user when the model loading has failed.
        """
        return self.__check_storage

    def __load_model(self):
        """
        A function that loads the model. The model should be contained in a pickle file
        """
        try:
            with open(self.model_path, "rb") as f:
                self.model = pickle.load(f)
                print(f"Model loaded successfully from {self.model_path}")
        except FileNotFoundError:
            self.is_task_failed = True
            print(f"Error: The file {self.model_path} was not found.")
            return None

    def __check_storage(self):
        """
        A function that checks if the file exists.
        If FileNotFoundError is already being retried, it prints a hint, otherwise enables retry.
        """
        if FileNotFoundError in self.exceptions_retry.keys() and self.exceptions_retry[FileNotFoundError()]:
            print("Check if you saved the model and if you did, check where did you saved it")
        else:
            self.exceptions_retry[FileNotFoundError()] = True


@app.post("/predictions")
def get_predictions(user_input: Any | None, task_id: str, max_retries: int, name: str, exceptions_retry: dict[Exception, bool], model_path: str):
    model_task = DefaultModelTask(task_id,max_retries ,name, exceptions_retry,model_path)
    deploy_uvicorn()
    return model_task.action(user_input)