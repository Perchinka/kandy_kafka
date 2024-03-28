# Abstract view class
from abc import ABC, abstractmethod

class AbstractView(ABC):
    @abstractmethod
    def display_output(self, brokers):
        raise NotImplementedError