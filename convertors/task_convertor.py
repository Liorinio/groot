from airflow.providers.standard.operators.python import PythonOperator
from basics.task import Task
from convertors.convertors import AirflowConvertor


class AirflowTaskConvertor(AirflowConvertor):

    def __init__(self, task: Task):
        """
        The AirflowTaskConvertor's constructor.
        It receives a Dag
        """
        self.task = task

    def convert(self) -> PythonOperator:
        pass

    def convert_with_input(self, **context):
        """
        The function allows to convert a Dag to an Airflow Dag
        """

