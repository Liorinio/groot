from datetime import datetime
from task import Task
from start_conditon import StartCondition
from cache_type import CacheType

class Dag:
    def __init__(self, dag_id:int, name:str, start_condition:StartCondition,start_time:datetime,
                 cache_type:CacheType,tasks: dict[Task, list[Task]], exit_point_persistent:bool):
        self.dag_id = dag_id
        self.name = name
        self.start_condition = start_condition
        self.start_time = start_time
        self.tasks = tasks
        self.cache_type = cache_type
        self.exit_point_persistent = exit_point_persistent

    def strat_trigger(self):
        ...

    def add_task(self, tasks_dict: dict[Task,list[Task]]):
        ...