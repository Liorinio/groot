from basics.task import Task
from convertors.convertors import AirflowConvertor


class AirflowTaskConvertor(AirflowConvertor):

    def __init__(self, task: Task):
        """
        The AirflowTaskConvertor's constructor.
        It receives a Dag
        """
        self.task = task

    def convert(self):
        """
        The function allows to convert a Task to an Airflow Task
        """
        pass
