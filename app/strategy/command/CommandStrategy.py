from abc import ABC, abstractmethod


class CommandStrategy(ABC):
    @abstractmethod
    def execute(self, data: list):
        raise NotImplementedError("Subclasses must implement this method")