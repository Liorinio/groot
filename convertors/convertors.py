from abc import ABC, abstractmethod


class Convertor(ABC):

    @abstractmethod
    def convert(self):
        pass


class AirflowConvertor(Convertor):

    def convert(self):
        pass
