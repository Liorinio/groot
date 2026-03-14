from typing import Any
<<<<<<< HEAD
from airflow.providers.standard.operators.python import PythonOperator
=======
>>>>>>> dev
from basics.task import Task
from convertors.convertors import AirflowConvertor


class AirflowTaskConvertor(AirflowConvertor):

    def __init__(self, task: Task, user_input: Any):
        """
        The AirflowTaskConvertor's constructor.
        It receives a Dag
        """
        self.user_input = user_input
        self.task = task

    def convert(self):
<<<<<<< HEAD
        pass

    def convert_with_input(self,input:Any|None) -> PythonOperator:
        pass
=======
        """
        The function allows to convert a Dag to an Airflow Dag
        """

>>>>>>> dev
