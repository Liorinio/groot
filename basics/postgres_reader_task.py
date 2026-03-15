from typing import Callable, Any
from task import Task
import psycopg2
import pandas as pd

class PostgresReaderTask(Task):

    def __init__(self, task_id: int, max_retries: int, name: str, exceptions_retry: dict[Exception, bool], connection_details: dict[str, str]):
        super().__init__(task_id, max_retries, name, exceptions_retry)

        """
        The class's constructor. It receives the same parameters as its parent class in addition to a path to where the model is saved
        """
        self.model = None
        self.connection_details = connection_details

    def action(self, user_input: Any | None):
        self.connect_to_postgres()

    def on_failure(self) -> Callable:
        def check_details():
            print("Check your connection details")
        return check_details()



    def dataframe_from_postgres(self, cursor, records):
        column_names = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(records, columns=column_names)
        return df


    def connect_to_postgres(self):
        connection = psycopg2.connect(database=self.connection_details["database"], user=self.connection_details["user"],
                                      password=self.connection_details["password"],host=self.connection_details["host"],port=int(self.connection_details["port"]))

        cursor = connection.cursor()
        records = self.execute_select_query(cursor)
        return self.dataframe_from_postgres(cursor, records)


    def execute_select_query(self, cursor):
        db_schema = self.connection_details["schema"]
        table_name = self.connection_details["table"]
        table_location = db_schema + "." + table_name
        cursor.execute(query=f"SELECT * FROM {table_location}")
        record = cursor.fetchall()
        return record





