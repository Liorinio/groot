from typing import Any
from airflow.providers.standard.operators.python import PythonOperator
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
        pass

    def convert_with_input(self, input:Any | None) -> PythonOperator:
        """
        The function allows to convert a Dag to an Airflow Dag
        """

