from datetime import datetime

from basics.dag import Dag
from basics.start_conditon import StartCondition
from cache_type import CacheType
from convertors.convertors import Convertor
from deployer.deployer import Deployer


class Client:

    def create_dag(self,dag_id:str,name:str,start_condition:StartCondition,start_time:datetime,cache_type:CacheType,exit_point_persistent:bool) -> Dag:
        """
        The 'create_dag()' function prompts the user for all the required parameters
        and returns a configured Dag object ready to be deployed.
        """
        return Dag(
            dag_id=dag_id,
            name=name,
            start_condition=start_condition,
            start_time=start_time,
            cache_type=cache_type,
            tasks={},
            exit_point_persistent=exit_point_persistent,
        )

    def deploy(self, deployer: Deployer) -> bool:
        """
        The 'deploy()' function gets a deployer and uses it to deploy the dag,
        returning True on success and False on failure.
        """
        return deployer.deploy()

    def convert(self, convertor: Convertor):
        """
        The 'convert()' function gets a convertor and uses it to convert the dag
        to the required format.
        """
        return convertor.convert()