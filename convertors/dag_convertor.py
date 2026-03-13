from basics.dag import Dag
from basics.task import Task
from convertors.convertors import AirflowConvertor
from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator

from convertors.task_convertor import AirflowTaskConvertor 

class AirflowDagConverter(AirflowConvertor):

    def __init__(self, dag: Dag):
        self.dag = dag

    def convert(self):
        created_dag = DAG(
            dag_id= self.dag.dag_id
            start_date= self.dag.
        )
    
        


        return created_dag
    
    def _create_python_operator_from_task(task_convertor:AirflowTaskConvertor):
        task = PythonOperator(task_id= task_convertor.task.task_id,
                               python_callable=task_convertor.convert)
        return task
    



    def set_task_dependencies(self,task: PythonOperator):
        task.set_downstream

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
