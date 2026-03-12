from basics.dag import Dag
from basics.task import Task
from convertors.convertors import AirflowConvertor


class AirflowDagConverter(AirflowConvertor):

    def __init__(self, dag: Dag):
        self.dag = dag

    def convert(self):
        pass

    def _find_first_task(self) -> Task:
        tasks = self.dag.tasks
        list_tasks = tasks.values()
        set_tasks:set = set()
        for tasks in list_tasks:
            for task in tasks:
                set_tasks.add(task)

        key_tasks = tasks.keys()
        for task in key_tasks:
            if task not in set_tasks:
                return task

    def _validate_task_order(self):
        ...
