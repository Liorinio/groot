from basics.dag import Dag
from convertors.convertors import AirflowConvertor


class AirflowDagConverter(AirflowConvertor):

    def __init__(self, dag: Dag):
        self.dag = dag

    def convert(self):
        pass

    def create_order(self):
        pass
