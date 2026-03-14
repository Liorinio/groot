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

    def convert(self):
        created_dag = DAG(
            dag_id= self.dag.dag_id
            start_date= self.dag.
        )
    
        


        return created_dag
    


    def _convert_first_pytask_to_airflow_task(self) -> PythonOperator:
        task = self._find_first_task
        convertor = AirflowTaskConvertor(task)
        converted_task = convertor.convert(None)
        return converted_task

    def _convert_pytasks_to_airflow_tasks(self) -> dict[PythonOperator, list[PythonOperator]]:
        first_task:PythonOperator = self._convert_first_pytask_to_airflow_task()
        set_airflow_tasks:set ={first_task.dag_id}
        airflow_tasks: dict[PythonOperator, list[PythonOperator]] = {first_task:[]}
        tasks = self.dag.tasks
        

        for key in tasks.keys():
            depend_tasks:list[PythonOperator] =[]
            if key.task_id not in set_airflow_tasks:
                task = AirflowTaskConvertor(self._get_task_by_id(key.task_id)).convert()
                set_airflow_tasks.add(task.task_id)
                airflow_tasks[task] = []
            for depend_task in tasks.get(self._get_task_by_id(key.task_id)):
                if depend_task.task_id not in set_airflow_tasks:
                    converted_depend_task = AirflowTaskConvertor(self._get_task_by_id
                                                                 (depend_task.task_id)).convert()
                    set_airflow_tasks.add(converted_depend_task.task_id)
                    depend_tasks.append(converted_depend_task)
                    airflow_tasks[converted_depend_task] = []
                else:
                    set_airflow_tasks.add(depend_task.task_id)
            airflow_tasks[self._get_task_by_id(key.task_id)] = depend_tasks




               





    def _get_task_by_id(tasks:dict[PythonOperator, list[PythonOperator]],task_id:str) ->PythonOperator:
        for task in tasks.keys:
            if task.task_id == task_id:
                return task


    def set_task_dependencies(self,task: PythonOperator):
        task.set_downstream

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
