from abc import ABC, abstractmethod


class ParserStrategy(ABC):
    @abstractmethod
    def parse(self, data):
        raise NotImplementedError("Subclasses must implement this method")