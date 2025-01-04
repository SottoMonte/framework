import asyncio
import importlib
import re


import sys
if sys.platform == 'emscripten':
    #language = language.load_module(area="framework",service='service',adapter='language')
    flow = language.load_module(area="framework",service='service',adapter='flow')
    #port = language.load_module(area="application",service='port',adapter='storekeeper')
else:
    import framework.service.flow as flow
    import framework.service.language as language

#port.storekeeper
class storekeeper():

    def __init__(self,**constants):
        self.providers = constants['providers']
    
    # overview/view/get
    @flow.asynchronous(args=('model','identifier'),managers=('messenger',))
    async def overview(self, messenger, **constants):
        """
        Effettua una richiesta API generica.
        
        :param model: modello dati di ritorno
        :param identifier: key
        :return transaction: trasazione
        """
        operations = [] 
        repository = language.load_module(area="application",service='repository',adapter=constants['model'])
        mappa = dict()
        miss = []
        
        for provider in self.providers:
            profile = provider.config['profile'].upper()
            
            if profile in repository.location:
                #translated = language.translation(constants,repository.values,repository.mapper,profile)
                translated = {}
                payload = repository.payloads.get('view',{})
                #print(constants|translated)
                task = asyncio.create_task(provider.view(location=profile,fields=repository.mapper,path=repository.location[profile],payload=payload,**constants|translated))
                operations.append(task)
                mappa[task] = profile
        
        while operations:
            
            finished, unfinished = await asyncio.wait(operations, return_when=asyncio.FIRST_COMPLETED)
            
            for operation in finished:
                transaction = operation.result()
                if transaction != None and transaction['state']:
                    profile = [x.config['profile'].upper() for x in self.providers if mappa[operation] == x.config['profile'].upper()][0] #mappa[operation].config['profile'].upper()
                    result = transaction['result']
                    
                    translated = language.translation(result,repository.values,repository.mapper,profile)

                    if len(miss) != 0:
                        #translated_in = language.translation(result,repository.values,repository.keys_test,profile)
                        #print(translated)
                        vv = await self.put(prohibited=[profile],value=translated,**constants)
                        #print(vv,miss)

                    for task in unfinished:
                        task.cancel()
                    
                    #if unfinished:
                    #    await asyncio.wait(unfinished)
                    #await messenger.post(name="log",value=f"success get miss {miss}")
                    
                    return {'state': True,'action':'tree','result':translated}
                else:
                    miss.append(mappa[operation])
                    if len(operations) == 1:
                        #await messenger.post(name="log",value=f"failed get  miss {miss}")
                        return {'state': False,'action':'tree','parameter':constants,'remark':'not found data'}

            operations = unfinished

    # gather/read/get
    @flow.asynchronous(args=('model','identifier'),managers=('messenger',))
    async def gather(self, messenger, **constants):
        """
        Effettua una richiesta API generica.
        
        :param model: modello dati di ritorno
        :param identifier: key
        :return transaction: trasazione
        """
        operations = [] 
        repository = language.load_module(area="application",service='repository',adapter=constants['model'])
        mappa = dict()
        miss = []
        
        for provider in self.providers:
            profile = provider.config['profile'].upper()
            
            if profile in repository.location:
                #translated = language.translation(constants,repository.values,repository.mapper,profile)
                translated = {}
                payload = repository.payloads.get('read',None)
                #print(constants|translated)
                task = asyncio.create_task(provider.read(location=profile,fields=repository.mapper,path=repository.location[profile],payload=payload,**constants|translated))
                operations.append(task)
                mappa[task] = profile
        
        while operations:
            
            finished, unfinished = await asyncio.wait(operations, return_when=asyncio.FIRST_COMPLETED)
            
            for operation in finished:
                transaction = operation.result()
                if transaction != None and transaction['state']:
                    profile = [x.config['profile'].upper() for x in self.providers if mappa[operation] == x.config['profile'].upper()][0] #mappa[operation].config['profile'].upper()
                    result = transaction['result']
                    
                    translated = language.translation(result,repository.values,repository.mapper,profile)

                    if len(miss) != 0:
                        #translated_in = language.translation(result,repository.values,repository.keys_test,profile)
                        #print(translated)
                        vv = await self.put(prohibited=[profile],value=translated,**constants)
                        #print(vv,miss)

                    for task in unfinished:
                        task.cancel()
                    
                    #if unfinished:
                    #    await asyncio.wait(unfinished)
                    #await messenger.post(name="log",value=f"success get miss {miss}")
                    
                    return {'state': True,'action':'get','result':translated}
                else:
                    miss.append(mappa[operation])
                    if len(operations) == 1:
                        #await messenger.post(name="log",value=f"failed get  miss {miss}")
                        return {'state': False,'action':'get','parameter':constants,'remark':'not found data'}

            operations = unfinished
    
    # make/create/put
    @flow.asynchronous(args=('model','value'),managers=('messenger',))
    async def make(self, messenger, **constants):
        repository = language.load_module(area="application",service='repository',adapter=constants['model'])
        prohibited = constants['prohibited'] if 'prohibited' in constants else []
        allowed = constants['allowed'] if 'allowed' in constants else []
        operations = []
        map_tasks = dict()
        # Adds operation if profile matches
        for provider in self.providers:
            profile = provider.config['profile'].upper()
            #print(profile,allowed)
            if profile not in prohibited and profile in repository.location:
                #if constants['value'] != None:
                #    constants['value'] = language.translation(constants['value'],repository.values,repository.mapper,'MODEL',profile)
                payload = repository.payloads.get('create',None)
                operations.append(provider.create(location=profile,payload=payload, path=repository.location[profile],**constants))
                map_tasks[len(operations)-1] = profile

        # Commit all operations at the same time   
        transactions = await asyncio.gather(*operations)
        if len(transactions) == 0:
            return self.builder('transaction',{'state': False,'action':'put','parameter':constants})
        
        state = all([transaction['state'] for transaction in transactions])
        result = [transaction['result'] for transaction in transactions if not transaction['state']]
        failed = [map_tasks[key] for key,transaction in enumerate(transactions) if not transaction['state']]
 
        # Rollback and return transaction based on the state
        if state:
            #await messenger.post(name="log",value=f"success put miss {failed}") 
            return {'state': True,'action':'put','remark':f"succeeded put "}
        else:
            #await messenger.post(name="log",value=f"failed put miss {failed}")
            if len(failed) != len(transactions) and len(failed) != 0:
                transaction = await self.pull(prohibited=failed,**constants)
                return self.builder('transaction',{'state': False,'action':'put','result':result[0],'parameter':constants,'transaction':transactions+[transaction]})
            else:
                return self.builder('transaction',{'state': False,'action':'put','result':result[0],'parameter':constants,'transaction':transactions})
            
    # has
    @flow.asynchronous(args=('model','identifier'))
    async def has(self,**constants):
        repository = importlib.import_module(f"framework.repository.{constants['model']}", package=None)
        prohibited = constants['prohibited'] if 'prohibited' in constants else [] 
        operations = []  
        # Adds operation if profile matches
        for provider in self.providers:
            profile = provider.config['profile'].upper()
            if profile in repository.location and profile not in prohibited:
                operations.append(provider.delete(path=repository.location[profile],location=profile,**constants))
        
        # Commit all operations at the same time  
        transactions = await asyncio.gather(*operations)

        state = all([transaction['state'] for transaction in transactions])
        # Construct and return a transaction based on the state
        if state:
            return self.builder('transaction',{'state': True,'action':'pull','remark':"",'parameter':constants})
        else:
            return self.builder('transaction',{'state': False,'action':'pull','parameter':constants,'transaction':transactions[0],'remark':f"error"})
    
    # pull/delete/delete
    @flow.asynchronous(args=('model','identifier'),managers=('messenger',))
    async def erase(self, messenger, **constants):
        repository = language.load_module(area="application",service='repository',adapter=constants['model'])
        prohibited = constants['prohibited'] if 'prohibited' in constants else [] 
        operations = []  
        # Adds operation if profile matches
        for provider in self.providers:
            profile = provider.config['profile'].upper()
            if profile in repository.location and profile not in prohibited:
                payload = repository.payloads.get('delete',None)
                operations.append(provider.delete(path=repository.location[profile],payload=payload,location=profile,**constants))
        
        # Commit all operations at the same time  
        transactions = await asyncio.gather(*operations)

        state = all([transaction['state'] for transaction in transactions if transaction != None])
        
        # Construct and return a transaction based on the state
        if state:
            #await messenger.post(name="log",value=f"success delete {constants['identifier']}")
            return {'state': True,'action':'pull','remark':"",'parameter':constants}
        else:
            
            return {'state': False,'action':'pull','parameter':constants,'transaction':transactions[0],'remark':f"error"}
    
    # change/update/patch
    @flow.asynchronous(args=('model','value','identifier'))
    async def change(self,**constants):
        repository = language.load_module(area="application",service='repository',adapter=constants['model'])
        prohibited = constants['prohibited'] if 'prohibited' in constants else []
        operations = []
        map_tasks = dict()
        # Adds operation if profile matches
        for provider in self.providers:
            profile = provider.config['profile'].upper()
            if profile in repository.location and profile not in prohibited:
                payload = repository.payloads.get('update',None)
                #vv = language.translation(constants,repository.values,repository.mapper,'MODEL',profile)
                operations.append(provider.update(location=profile,payload=payload, path=repository.location[profile], **constants))
                map_tasks[len(operations)-1] = profile

        # Commit all operations at the same time   
        transactions = await asyncio.gather(*operations)
        
        state = all([transaction['state'] for transaction in transactions])
        #result = [transaction['result'] for transaction in transactions if not transaction['state']]
        #failed = [map_tasks[key] for key,transaction in enumerate(transactions) if not transaction['state']]

        # Rollback and return transaction based on the state
        if state:
            return {'state': True,'action':'put','remark':f"succeeded put"}
        else:
            return {'state': False,'action':'put','remark':f"error"}
            '''if len(failed) != len(transactions) and len(failed) != 0:
                transaction = await self.pull(prohibited=failed,**constants)
                return self.builder('transaction',{'state': False,'action':'put','result':result[0],'parameter':constants,'transaction':transactions+[transaction]})
            else:
                return self.builder('transaction',{'state': False,'action':'put','result':result[0],'parameter':constants,'transaction':transactions})'''