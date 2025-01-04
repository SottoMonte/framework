
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

import sys
if sys.platform == 'emscripten':
    flow = language.load_module(area="framework",service='service',adapter='flow')
else:
    import framework.service.flow as flow

class messenger():

    def __init__(self,**constants):
        self.providers = constants['providers']

    
    def post_sync(self,**constants):
        print(constants)
        #asyncio.create_task(self.post(**constants))

    @flow.asynchronous(args=('model','value'))
    async def post(self,**constants):
        prohibited = constants['prohibited'] if 'prohibited' in constants else []
        allowed = constants['allowed'] if 'allowed' in constants else []
        operations = []
        map_tasks = dict()
        # email -> email | log,fs -> messaggio | app -> evento
        #sender, receiver 
        receiver = None

        # Adds operation if profile matches
        for provider in self.providers:
            profile = provider.config['profile'].upper()
            #can = await provider.can(**constants)
            #if can or profile in allowed:
            operations.append(provider.post(location=profile, **constants))
            map_tasks[len(operations)-1] = profile

        # Commit all operations at the same time   
        transactions = await asyncio.gather(*operations)
        
        #state = all([transaction['state'] for transaction in transactions])
        #result = [transaction['result'] for transaction in transactions if not transaction['state']]
        #failed = [map_tasks[key] for key,transaction in enumerate(transactions) if not transaction['state']]

        
        '''if state:
            #return self.builder('transaction',{'state': True,'action':'post','remark':f"succeeded put {constants['identifier']}"})
            return state
        else:
            #return self.builder('transaction',{'state': False,'action':'post','result':result[0],'parameter':constants,'transaction':transactions})
            return state'''

    @flow.asynchronous(args=('model','value'))
    async def read(self,**constants):
        prohibited = constants['prohibited'] if 'prohibited' in constants else []
        allowed = constants['allowed'] if 'allowed' in constants else ['FAST']
        operations = []

        for provider in self.providers:
            profile = provider.config['profile'].upper()
            if profile in allowed:
                task = asyncio.create_task(provider.get(location=profile,**constants))
                operations.append(task)
        
        while operations:
            
            finished, unfinished = await asyncio.wait(operations, return_when=asyncio.FIRST_COMPLETED)
            
            
            for operation in finished:
                transaction = operation.result()
                if transaction['state']:
                    result = transaction['result']

                    for task in unfinished:
                        task.cancel()
                    if unfinished:
                        await asyncio.wait(unfinished)
                    
                    return result
                else:
                    if len(operations) == 1:
                        return transaction

            operations = unfinished