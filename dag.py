from task import Task

class Dag:
    def __init__(self, dag_id, name, start_time, tasks, exit_point_persistent):
        self.dag_id = dag_id
        self.name = name
        self.start_time = start_time
        self.tasks = tasks
        self.exit_point_persistent = exit_point_persistent

        #how to add the enums to the constructor

    def strat_trigger(self):
        ...

    def add_task(self, tasks_dict: dict[Task,list[Task]]):
        ...