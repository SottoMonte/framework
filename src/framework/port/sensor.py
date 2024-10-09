from abc import ABC, abstractmethod

class port(ABC):

    @abstractmethod
    def loader(self,*services,**constants):
        pass

    @abstractmethod
    async def detect(self,*services,**constants):
        pass