#select.work.value = value
#'\clients' == 'clients.' 
#'\clients\C00011608' == 'clients.C00011608'
#'\clients\C00011608' = view | 'clients.C00011608' = data == 'api\clients\C00011608'

'''
Una classe storekeeper in Python pu� essere utilizzata per rappresentare un gestore di magazzino o un custode di magazzino. Ecco alcuni compiti che una classe storekeeper potrebbe svolgere:

Gestione dell�inventario:
Un storekeeper pu� tenere traccia degli articoli presenti nel magazzino, aggiungendo nuovi elementi e rimuovendo quelli esauriti.
Pu� gestire quantit�, codici di prodotto, descrizioni e altre informazioni relative agli articoli.

Registrazione delle transazioni:
Il storekeeper pu� registrare le entrate e le uscite di merci dal magazzino.
Ad esempio, quando un prodotto viene consegnato o spedito, il storekeeper registra la transazione.

Controllo delle scorte:
Monitora i livelli di inventario per evitare carenze o eccessi.
Se le scorte di un articolo scendono al di sotto di una soglia, il storekeeper pu� avvisare o rifornire il magazzino.

Organizzazione fisica del magazzino:
Il storekeeper pu� pianificare la disposizione degli articoli nel magazzino per massimizzare l�efficienza e facilitare la ricerca.
Ad esempio, posizionare gli articoli pi� richiesti in posizioni accessibili.

Comunicazione con fornitori e clienti:
Il storekeeper pu� gestire gli ordini, le consegne e le restituzioni.
Comunica con i fornitori per rifornire il magazzino e con i clienti per risolvere eventuali problemi.

Memorizzazione di dati o informazioni: Una classe �memorizer� potrebbe essere progettata per gestire la memorizzazione e il recupero di dati o informazioni. Ad esempio, potrebbe essere utilizzata per archiviare e recuperare dati temporanei o configurazioni.
Gestione di cache o buffer: In programmazione, una classe �memorizer� potrebbe essere utilizzata per implementare una cache o un buffer per migliorare le prestazioni. Ad esempio, potrebbe memorizzare risultati di calcoli costosi per evitare di ricalcolarli ogni volta.
Supporto per operazioni di copia o clonazione: Una classe �memorizer� potrebbe essere coinvolta nella copia o clonazione di oggetti o strutture dati. Potrebbe mantenere traccia di oggetti duplicati o di copie temporanee.
'''

from abc import ABC, abstractmethod

class storekeeper(ABC):

    

    def __init__(self,**constants):
        pass
    
    @abstractmethod
    def builder(self,schema,value=None,spread={}):
        pass

    @abstractmethod
    def translation(self,constants,values,keys,input='MODEL',output='MODEL'):
        pass
    
    @abstractmethod
    async def get(self, messenger, **constants):
        pass

    @abstractmethod
    async def put(self, messenger, **constants):
        pass
            
    @abstractmethod
    async def has(self,**constants):
        pass
    
    @abstractmethod
    async def pull(self, messenger, **constants):
        pass
    
    @abstractmethod
    async def change(self,**constants):
        pass