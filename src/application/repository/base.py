from abc import ABC, abstractmethod

class DataMapper(ABC):
    @abstractmethod
    def map_to_domain(self, data: dict) -> object:
        """Trasforma i dati esterni in un'istanza del modello di dominio."""
        pass

    @abstractmethod
    def map_to_external(self, domain_model: object) -> dict:
        """Trasforma un'istanza del modello di dominio in dati esterni."""
        pass