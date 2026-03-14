from abc import ABC, abstractmethod

class Deployer(ABC):

    @abstractmethod
    def deploy(self) -> bool:
        """
        The 'deploy()' function deploys the target resource and returns True on success, False on failure.
        """
        pass