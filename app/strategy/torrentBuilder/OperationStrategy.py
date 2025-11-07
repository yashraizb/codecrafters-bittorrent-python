from abc import ABC, abstractmethod


class OperationStrategy(ABC):

    @abstractmethod
    def execute(self):
        pass