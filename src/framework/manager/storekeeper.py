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
    import application.port.storekeeper as port
    import framework.service.language as language

#port.storekeeper
class storekeeper():

    def __init__(self,**constants):
        self.providers = constants['providers']
        pass
    
    def builder(self,schema,value=None,spread={}):
        output = dict({})
        order = ['type','model','iterable','default','regex']
        if type(schema) == type(tuple()):
            for row in schema:
                name = row['name'] if 'name' in row else '@'
                
                if 'model' in row:
                    name = row['model'][0]['name'] if 'name' in row['model'][0] and 'name' not in row else name
                a = self.builder(row,value,spread)
                output[name] = a
        elif type(schema) == type(''):
            if ':' in schema:
                splited = schema.split(':')
                #print(splited)
                model = importlib.import_module(f"application.{splited[0]}.{splited[1]}", package=None)
                output |= self.builder(getattr(model,splited[1]),value)
            else:
                model = importlib.import_module(f"application.model.{schema}", package=None)
                output |= self.builder(getattr(model,schema),value)
        else:
            for field in order:
                if field in schema:
                    
                    valore = schema[field]
                    #if 'model' in schema: schema.pop('model')
                    #print(schema,spread)
                    name = schema['name'] if 'name' in schema else ''
                    if name == '' and 'name' in spread:
                        name = spread['name']
                    if 'model' in schema:
                        name = schema['model'][0]['name'] if 'name' in schema['model'][0] and 'name' not in schema else name
                    #print(field,valore,name)
                    
                    match field:
                        case 'iterable':
                            if valore:
                                output[name] = []
                        case 'model':
                            #name = valore[0]['name'] if 'name' in valore[0] else ''
                            #print('??',name,valore[0])  
                            if type(dict()) != type(value):
                                passa = value
                            elif name in value:
                                passa = value[name]
                            else:
                                passa = None

                            output[name] = self.builder(valore,passa,schema)
                        case 'type':
                            if valore == 'string':
                                output[name] = ''
                            if valore == 'integer':
                                output[name] = 0
                            if valore == 'model':
                                output[name] = dict()
                        case 'default':
                            if type(value) == type(dict()):
                                if name in value:
                                    ccc = value[name]
                                else:
                                    ccc = valore
                            else:
                                ccc = value
                            
                            if type(ccc) in [type(list()),type(dict())] and type(ccc) != type(schema['type']):
                                for x in ccc:
                                    if type(x) ==  type(schema['type']):
                                         output[name].append(x)
                                    if type(schema['type']) == type(tuple()) and type(x) == type(dict()):
                                        a = self.builder(schema['type'],x)
                                        if type(a) != type(dict()) :
                                            output[name].append(a)
                                        elif len(a) != 0:
                                             output[name].append(a)
                                        
                            elif 'type' in schema and type(ccc) == type(schema['type']) :
                                output[name] = ccc
                            else:
                                 output[name] = valore
                        case 'regex':
                            pattern = re.compile(valore)
                            if name in output:
                                check = output[name] if type(output[name]) != type(dict()) else ''
                            else: check = ''
                            if check != '' and not pattern.match(str(check)):
                                #print(check)
                                raise Exception(f"Regex not match {valore}")
                                            
        if len(output) == 1:
            return output[next(iter(output))]
        else: return output

    def translation(self,constants,values,keys,input='MODEL',output='MODEL'):
        
        out = dict()
        zwork = dict()

        for x in constants:
            #print(x,constants)
            zwork |= language.put(x,constants[x],zwork)
        #print(input,output,constants)
        for row in keys:
            if not input in row: dd = row['MODEL']
            else:dd = row[input]
            if not output in row: name = row['MODEL']
            else:name = row[output]

            trat = row['MODEL'] if dd not in row else dd

            if type(dd) == type([]):
                for x in dd:
                   valor = language.get(x,zwork)
                   #valor = [1,2,3] 
                   if valor != None:break
            else:valor = language.get(dd,zwork)
            #print(name,dd,valor,'<====')
            if valor != None:
                #print(input,output,row,dd,trat)
                if trat in values:
                    for x in values[trat]:
                        #print(x)
                        if type(x[output]) == type(""):
                            pass
                        else:
                            valor = x[output](valor)
                    #print(valor)
                out |= language.put(name,valor,out)
            #print(dd,valor)'''
        
        return out
    
    # get/read/get
    @flow.async_function(args=('model','identifier'),ports=('messenger',))
    async def get(self, messenger, **constants):
        
        operations = [] 
        repository = language.load_module(area="framework",service='repository',adapter=constants['model'])
        mappa = dict()
        miss = []
        
        for provider in self.providers:
            profile = provider.config['profile'].upper()
            
            if profile in repository.location:
                translated = self.translation(constants,repository.values,repository.keys_test,'MODEL',profile)
                #print(constants|translated)
                task = asyncio.create_task(provider.read(location=profile,fields=repository.keys_test,path=repository.location[profile],**constants|translated))
                operations.append(task)
                mappa[task] = profile
        
        while operations:
            
            finished, unfinished = await asyncio.wait(operations, return_when=asyncio.FIRST_COMPLETED)
            
            for operation in finished:
                transaction = operation.result()
                if transaction != None and transaction['state']:
                    profile = [x.config['profile'].upper() for x in self.providers if mappa[operation] == x.config['profile'].upper()][0] #mappa[operation].config['profile'].upper()
                    result = transaction['result']
                    
                    translated = self.translation(result,repository.values,repository.keys_test,profile)

                    if len(miss) != 0:
                        #translated_in = self.translation(result,repository.values,repository.keys_test,profile)
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
        
    
    # put/create/post
    @flow.async_function(args=('model','value'),ports=('messenger',))
    async def put(self, messenger, **constants):
        repository = importlib.import_module(f"framework.repository.{constants['model']}", package=None)
        prohibited = constants['prohibited'] if 'prohibited' in constants else []
        allowed = constants['allowed'] if 'allowed' in constants else []
        operations = []
        map_tasks = dict()
        # Adds operation if profile matches
        for provider in self.providers:
            profile = provider.config['profile'].upper()
            #print(profile,allowed)
            if profile not in prohibited and profile in repository.location:
                if constants['value'] != None:
                    constants['value'] = self.translation(constants['value'],repository.values,repository.keys_test,'MODEL',profile)
                operations.append(provider.create(location=profile, **constants, path=repository.location[profile]))
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
            await messenger.post(name="log",value=f"success put miss {failed}") 
            return self.builder('transaction',{'state': True,'action':'put','remark':f"succeeded put "})
        else:
            await messenger.post(name="log",value=f"failed put miss {failed}")
            if len(failed) != len(transactions) and len(failed) != 0:
                transaction = await self.pull(prohibited=failed,**constants)
                return self.builder('transaction',{'state': False,'action':'put','result':result[0],'parameter':constants,'transaction':transactions+[transaction]})
            else:
                return self.builder('transaction',{'state': False,'action':'put','result':result[0],'parameter':constants,'transaction':transactions})
            
    # has
    @flow.async_function(args=('model','identifier'))
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
    @flow.async_function(args=('model','identifier'),ports=('messenger',))
    async def pull(self, messenger, **constants):
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

        state = all([transaction['state'] for transaction in transactions if transaction != None])
        
        # Construct and return a transaction based on the state
        if state:
            await messenger.post(name="log",value=f"success delete {constants['identifier']}")
            return self.builder('transaction',{'state': True,'action':'pull','remark':"",'parameter':constants})
        else:
            await messenger.post(name="log",value=f"failed delete {constants['identifier']}")
            return self.builder('transaction',{'state': False,'action':'pull','parameter':constants,'transaction':transactions[0],'remark':f"error"})
    
    # add/write/patch
    @flow.async_function(args=('model','value','identifier'))
    async def change(self,**constants):
        repository = importlib.import_module(f"framework.repository.{constants['model']}", package=None)
        prohibited = constants['prohibited'] if 'prohibited' in constants else []
        operations = []
        map_tasks = dict()
        # Adds operation if profile matches
        for provider in self.providers:
            profile = provider.config['profile'].upper()
            if profile in repository.location and profile not in prohibited:
                vv = self.translation(constants['value'],repository.values,repository.keys_test,'MODEL',profile)
                operations.append(provider.write(location=profile, identifier=constants['identifier'], model=constants['model'], path=repository.location[profile], value=vv))
                map_tasks[len(operations)-1] = profile

        # Commit all operations at the same time   
        transactions = await asyncio.gather(*operations)
        
        state = all([transaction['state'] for transaction in transactions])
        result = [transaction['result'] for transaction in transactions if not transaction['state']]
        failed = [map_tasks[key] for key,transaction in enumerate(transactions) if not transaction['state']]

        # Rollback and return transaction based on the state
        if state:
            return self.builder('transaction',{'state': True,'action':'put','remark':f"succeeded put {constants['identifier']}"})
        else:
            if len(failed) != len(transactions) and len(failed) != 0:
                transaction = await self.pull(prohibited=failed,**constants)
                return self.builder('transaction',{'state': False,'action':'put','result':result[0],'parameter':constants,'transaction':transactions+[transaction]})
            else:
                return self.builder('transaction',{'state': False,'action':'put','result':result[0],'parameter':constants,'transaction':transactions})