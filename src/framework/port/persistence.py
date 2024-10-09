from abc import ABC, abstractmethod

class port(ABC):

    @abstractmethod
    def read(self,*services,**constants):
        """
        Restituisce True se la stringa è un indirizzo email valido, altrimenti False.

        Args:
            file (str): La stringa da verificare come indirizzo email.

        Returns:
            str: True se la stringa è un indirizzo email valido, altrimenti False.
        """
        pass

    @abstractmethod
    async def create(self,*services,**constants):
        pass

    @abstractmethod
    async def delete(self,*services,**constants):
        pass

    @abstractmethod
    async def write(self,*services,**constants):
        pass

    @abstractmethod
    async def query(self,*services,**constants):
        pass

    @abstractmethod
    async def tree(self,*services,**constants):
        """
        Restituisce True se la stringa è un indirizzo email valido, altrimenti False.

        Args:
            path (str): La stringa da verificare come indirizzo email.

        Returns:
            tuple: True se la stringa è un indirizzo email valido, altrimenti False.
        """
        pass