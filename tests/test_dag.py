import sys
sys.path.append("/mnt/c/Users/Noago/finalprolect/groot")
print(sys.path)
import json
import datetime
from typing import Any, Callable
import requests
from basics.task import Task
from basics.dag import Dag
from basics.start_conditon import StartCondition
from cache_type import CacheType
from client.client import Client
from convertors.dag_convertor import AirflowDagConverter


class GetCatFact(Task):
    def on_failure(self) -> Callable:
        pass

    def action(self, user_input: Any | None):
        url = "http://catfact.ninja/fact"
        res = requests.get(url)
        return {"cat_fact": json.loads(res.text)["fact"]}


class PrintTheCatFact(Task):
    def on_failure(self) -> Callable:
        pass

    def action(self, user_input: Any | None):
        print(user_input)


task1 = GetCatFact(2, "task1", {Exception(): False})
task2 = PrintTheCatFact(2, "task2", {Exception(): False})

dag = Dag("dag", StartCondition.DATE, datetime.datetime(2026, 3, 15, 15, 0), CacheType.NONE, {task1:[task2]}, False)

convertor = AirflowDagConverter(dag)
client = Client()
airflow_dag = client.convert(convertor=convertor)

"""
client = Client()
airflow_dag = client.convert(convertor=convertor)
deployer = AirflowDeployer(airflow_dag,"https://github.com/DanitSi112/dags.git","/mnt/c/Users/Noago/finalprolect/groot/created_dags")
client.deploy(deployer=deployer)
print(airflow_dag())
"""
