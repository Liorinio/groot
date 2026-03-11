from basics.task import Task
from convertors.convertors import AirflowConvertor


class AirflowTaskConvertor(AirflowConvertor):

    def __init__(self, task: Task):
        self.task = task

    def convert(self):
        pass
