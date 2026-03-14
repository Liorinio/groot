from airflow.providers.standard.operators.python import PythonOperator
from basics.task import Task
from convertors.convertors import AirflowConvertor


class AirflowTaskConvertor(AirflowConvertor):

    def __init__(self, task: Task, dag_id: str, depended_task_id: str):
        """
        The AirflowTaskConvertor's constructor.
        It receives a Task
        """
        self.task = task
        self.dag_id = dag_id
        self.depended_task_id = depended_task_id

    def convert(self) -> PythonOperator:
        """
        The function creates a python operator from the convert_with_input() function
        """

    def wrapped_action(self, **context):
        """
        The function wraps the clients task with the s3 writer and reader
        """

