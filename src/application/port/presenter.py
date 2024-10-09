from abc import ABC, abstractmethod

class presenter(ABC):
    
    @abstractmethod
    async def builder(self,**constants):
        pass
        
    @abstractmethod
    async def description(self,**constants):
        pass
        
    @abstractmethod
    async def benchmark(self,**constants):
        pass

    @abstractmethod
    async def effort(self,**constants):
        pass