
''' 
Una classe Messenger in Python pu� essere utilizzata per gestire la comunicazione tra diverse parti di un�applicazione. Ecco alcuni possibili compiti che una classe Messenger potrebbe svolgere:

Comunicazione tra componenti:
Una classe Messenger pu� fungere da intermediario per la comunicazione tra diverse parti del codice. Ad esempio, se hai pi� classi o moduli che devono scambiarsi informazioni, puoi utilizzare una classe Messenger per gestire i messaggi tra di loro.

Gestione degli eventi:
Puoi utilizzare una classe Messenger per implementare un sistema di eventi. Le altre classi possono registrarsi per ricevere notifiche quando si verificano determinati eventi.
Ad esempio, se stai sviluppando un�app di gioco, potresti avere una classe Messenger che gestisce gli eventi di collisione tra oggetti nel gioco.

Sincronizzazione di stato:
Se hai pi� componenti che condividono lo stesso stato (ad esempio, variabili globali o dati di configurazione), una classe Messenger pu� aiutare a sincronizzare le modifiche allo stato.
Quando uno dei componenti modifica lo stato, pu� inviare un messaggio al Messenger, che quindi notifica gli altri componenti interessati.

Comunicazione remota:
Se hai bisogno di comunicare tra processi o tra computer, una classe Messenger pu� essere utilizzata per inviare messaggi attraverso una rete o tramite socket.

Implementazione di un sistema di chat:
Se stai sviluppando un�applicazione che richiede una chat o una messaggistica, una classe Messenger pu� gestire l�invio e la ricezione di messaggi tra utenti.
'''
import asyncio
from abc import ABC, abstractmethod

class messenger(ABC):

    def __init__(self,**constants):
        self.providers = [] 

    @abstractmethod
    async def post(self,**constants):
        pass
    
    @abstractmethod
    async def get(self,**constants):
        pass