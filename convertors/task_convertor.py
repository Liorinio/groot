from basics.task import Task
from convertors.convertors import AirflowConvertor


class AirflowTaskConvertor(AirflowConvertor):

    def __init__(self, task: Task):
        """
        The AirflowTaskConvertor's constructor.
        It receives a Task
        """
        self.task = task

    def convert(self):
        """
        The function creates a python operator from the convert_with_input() function
        """

    def convert_with_input(self, **context):
        """
        The function wraps the clients task with the s3 writer and reader
        """

