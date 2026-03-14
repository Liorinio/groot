from basics.dag import Dag
from basics.task import Task
from convertors.convertors import AirflowConvertor
from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator
from convertors.task_convertor import AirflowTaskConvertor 


class AirflowDagConverter(AirflowConvertor):

    def __init__(self, dag: Dag):
        """
        The AirflowDagConverter's constructor.
        It receives a Dag
        """
        self.dag = dag

    def _get_task_by_id(self, tasks:dict[PythonOperator, list[PythonOperator]],task_id:str) ->PythonOperator:
        for task in tasks.keys():
            if task.task_id == task_id:
                return task
            
    def _convert_single_pytask_to_airflow_tasks(self,tasks_id_set:set,task_id:str,
                                                tasks:dict[PythonOperator, list[PythonOperator]]) -> PythonOperator:
        task = AirflowTaskConvertor(self._get_task_by_id(tasks,task_id)).convert()
        tasks_id_set.add(task_id)
        return task

    def _convert_depend_tasks(self,python_tasks:list[Task],tasks_id_set:set,
                              dag_tasks:dict[PythonOperator,list[PythonOperator]])->list[PythonOperator]:
        
        depend_tasks:list[PythonOperator] =[]
        for depend_task in python_tasks:
            if depend_task.task_id not in tasks_id_set:
                converted_depend_task = self._convert_single_pytask_to_airflow_tasks(tasks_id_set,depend_task.task_id,
                                                                                     dag_tasks)
                depend_tasks.append(converted_depend_task)
                dag_tasks[converted_depend_task] = []
            else:
                tasks_id_set.add(depend_task.task_id)
        return depend_tasks

    def _convert_pytasks_to_airflow_tasks(self) -> dict[PythonOperator, list[PythonOperator]]:
        tasks_id_set:set = set()
        airflow_tasks: dict[PythonOperator, list[PythonOperator]] = {}
        tasks = self.dag.tasks

        for key in tasks.keys():
            depend_tasks:list[PythonOperator] =[]
            if key.task_id not in tasks_id_set:
                task = self._convert_single_pytask_to_airflow_tasks(tasks_id_set, key.task_id,airflow_tasks)
                airflow_tasks[task] = []
            depend_tasks = self._convert_depend_tasks(tasks.get(key),tasks_id_set,airflow_tasks)
            airflow_tasks[self._get_task_by_id(key.task_id)] = depend_tasks
        return airflow_tasks

    def _set_dependencies_for_tasks(self, tasks:dict[PythonOperator, list[PythonOperator]]):
        for task in tasks.keys():
            task.set_downstream(tasks.get(task))

    def _find_first_task(self) -> Task:
        """
        A function that finds and returns the first task in the dag
        :return:
        """
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
        """
        a function that checks if the dag is a validate one
        """
        ...

    def convert(self):
        created_dag = DAG(
            dag_id=self.dag.dag_id,
            start_date=self.dag.start_time
        )
        return created_dag
