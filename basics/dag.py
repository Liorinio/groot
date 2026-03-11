from datetime import datetime
from typing import Tuple, Optional
from basics.task import Task
from start_conditon import StartCondition
from cache_type import CacheType


def choice_options() -> str:
    options_dict = {1: "None", 2: "once", 3: "hourly", 4: "daily", 5: "weekly", 6: "monthly", 7: "yearly"}

    for key, value in options_dict.items():
        print(f"{key}: {value}")

    while True:
        choice = input("choose one of the presented options: ").strip()
        try:
            choice_number = int(choice)
            if 2 <= choice_number <= 7:
                return "@" + options_dict[choice_number]
            elif choice_number == 1:
                return options_dict[choice_number]
            else:
                print("Invalid input: please choose again")
        except ValueError:
            print("Invalid input: please choose again")


class Dag:
    """
    The Dag's constructor. it receives a number which represents the id of the dag, name for the dag, a start condition from the available start conditions of the library,
    a cache type from the available cache types of the library, a dictionary which contains a task as the key and list of all the tasks that depend on it as the value
    and a boolean parameter which defines if the output of the dag should be saved or not
    """
    def __init__(self, dag_id: int, name: str, start_condition: StartCondition, start_time: datetime,
                 cache_type: CacheType, tasks: dict[Task, list[Task]], exit_point_persistent: bool):
        self.dag_id = dag_id
        self.name = name
        self.start_condition = start_condition
        self.start_time = start_time
        self.tasks = tasks
        self.cache_type = cache_type
        self.exit_point_persistent = exit_point_persistent

    # defines start trigger
    def start_trigger(self) -> Tuple[datetime, Optional[str]]:
        if self.start_condition.name == "date":
            time_trigger = choice_options()
            return self.start_time, time_trigger
        elif self.start_condition.name == "trigger":
            return self.start_time, f"{self.name}_trigger"
        else:
            raise ValueError(f"Unsupported start condition: {self.start_condition}")

    """
    The 'add_task()' function get a task and a list of the tasks that depend on it and adds the task to the dag
    """
    def add_task(self, task: Task, depended_tasks: list[Task]):
        self.tasks[task] = depended_tasks
