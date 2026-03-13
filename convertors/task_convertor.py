from typing import Any
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
        """
        The function allows to convert a Dag to an Airflow Dag
        """

