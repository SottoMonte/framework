from abc import ABC, abstractmethod

class presentation(ABC):

    @abstractmethod
    def loader(self, *services, **constants):
        pass