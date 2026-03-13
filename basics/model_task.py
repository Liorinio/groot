import pickle
from typing import Callable, Any
from task import Task


def process(input_data,model):
    try:
        predictions = model.predict(input_data)
        return predictions

    except Exception as e:
        print(f"An error occurred during model loading or inference: {e}")
        return None


class DefaultModelTask(Task):
    def action(self, user_input: Any | None):
        self.__load_model()
        process(user_input, self.model)

    def on_failure(self) -> Callable:
        return self.__check_storage()

    def __init__(self,task_id: int,max_retries: int,name: str, exceptions_retry: dict[Exception, bool],model_path: str):
        super().__init__(task_id, max_retries, name, exceptions_retry)

        self.model_path = model_path
        self.model = None

    def __load_model(self):
        try:
            with open(self.model_path, "rb") as f:
                self.model = pickle.load(f)
                print(f"Model loaded successfully from {self.model_path}")
        except FileNotFoundError:
            print(f"Error: The file {self.model_path} was not found.")
            return None

    def __check_storage(self):
        if FileNotFoundError in self.exceptions_retry.keys() and self.exceptions_retry[FileNotFoundError]:
            print("check if you saved the model and if you did, check where did you saved it")



