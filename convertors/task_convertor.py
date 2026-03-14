from basics.task import Task
from convertors.convertors import AirflowConvertor
from airflow.providers.standard.operators.python import PythonOperator
from platforms.s3_handler import validate_s3_path, should_write_s3, read_from_s3, write_to_s3


class AirflowTaskConvertor(AirflowConvertor):

    def __init__(self, task: Task, dag_id: str, depended_task_id: str):
        """
        The AirflowTaskConvertor's constructor.
        It receives a Task
        """
        self.task = task
        self.dag_id = dag_id
        self.depended_task_id = depended_task_id

    def convert(self) -> PythonOperator:
        """
        The function creates a python operator from the convert_with_input() function
        """
        return PythonOperator(
            task_id=self.task.task_id,
            provide_context=True,
            xcom_push=True,
            python_callable=self.wrapped_action
        )

    def wrapped_action(self, **context):
        """
        The function wraps the clients task with the s3 writer and reader
        """
        ti = context["ti"]
        action_input = ti.xcom_pull(task_ids=self.depended_task_id)
        if action_input:
            if type(action_input) == str and validate_s3_path(action_input, self.dag_id, self.depended_task_id):
                action_input = read_from_s3(action_input)
        output = self.task.action(action_input)
        if should_write_s3(output):
            output = write_to_s3(output, self.task.task_id, self.dag_id)
        return output


