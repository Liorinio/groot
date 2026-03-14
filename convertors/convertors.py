from abc import ABC, abstractmethod


class Convertor(ABC):
    """
    abstract method that allows to convert
    """
    @abstractmethod
    def convert(self):
        pass


class AirflowConvertor(Convertor):
    """
    The function allows to convert object to their counterparts in Airflow
    """
    def convert(self):
        pass
