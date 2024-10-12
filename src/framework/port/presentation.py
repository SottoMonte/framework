from abc import ABC, abstractmethod

class presentation(ABC):

    @abstractmethod
    def loader(self, *services, **constants):
        pass

    async def builder(self, *services, **constants):
        pass
    
    async def rebuild(self, *services, **constants):
        pass

    async def mount(self, *services, **constants):
        pass