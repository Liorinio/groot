from typing import Any
from airflow.providers.standard.operators.python import PythonOperator
from basics.task import Task
from convertors.convertors import AirflowConvertor


class AirflowTaskConvertor(AirflowConvertor):

    def __init__(self, task: Task):
        self.task = task

    def convert(self):
        pass

    def convert_with_input(self,input:Any|None) -> PythonOperator:
        pass
