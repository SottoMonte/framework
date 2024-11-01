#import application.port.language as language
from collections import OrderedDict

from kink import di
import importlib
import tomli
import js
import sys
import os
from jinja2 import Environment

def ttt(**constants):
    adapter = constants['adapter'] if 'adapter' in constants else ''
    service = constants['service'] if 'service' in constants else ''
    area = constants['area'] if 'area' in constants else ''
    payload = constants['payload'] if 'payload' in constants else ''

    spec=importlib.util.spec_from_file_location(adapter,f"src/{area}/{service}/{adapter}.py")
 
    # creates a new module based on spec
    foo = importlib.util.module_from_spec(spec)

    spec_lang=importlib.util.spec_from_file_location('language','src/framework/service/language.py')
    foo_lang = importlib.util.module_from_spec(spec_lang)
    spec_lang.loader.exec_module(foo_lang)
    setattr(foo,'language',foo_lang)
    
    # executes the module in its own namespace
    # when a module is imported or reloaded.
    spec.loader.exec_module(foo)

    return foo

def loader_provider_test(**constants):
        adapter = constants['adapter'] if 'adapter' in constants else ''
        service = constants['service'] if 'service' in constants else ''
        payload = constants['payload'] if 'payload' in constants else ''
        area = constants['area'] if 'area' in constants else 'framework'
            
        req = js.XMLHttpRequest.new()
        req.open("GET", f"{area}/{service}/{adapter}.py", False)
        req.send()

        req2 = js.XMLHttpRequest.new()
        req2.open("GET", f"framework/service/language.py", False)
        req2.send()

        spec2 = importlib.util.spec_from_loader('language', loader=None)
        module2 = importlib.util.module_from_spec(spec2)
        exec(req2.response, module2.__dict__)
        
        spec = importlib.util.spec_from_loader(adapter, loader=None)
        module = importlib.util.module_from_spec(spec)
        module.language = module2
        exec(req.response, module.__dict__)

        

        return module
            
def load_module(**c):
    if sys.platform == 'emscripten':
        return loader_provider_test(**c)
    else:
        return ttt(**c)

async def get_module(path):
    #response = js.fetch(f'application/action/{act}.py',{'method':'GET'})
    response = js.fetch(path,{'method':'GET'})
    file = await response
    aa = await file.text()
    try:
        spec = importlib.util.spec_from_loader(act, loader=None)
        module = importlib.util.module_from_spec(spec)
        exec(aa, module.__dict__)
        return module
    except Exception as e:
        print(f"error load 'infrastructure module'")

async def loader_module(self,act):
    response = js.fetch(f'application/action/{act}.py',{'method':'GET'})
    file = await response
    aa = await file.text()
    try:
        spec = importlib.util.spec_from_loader(act, loader=None)
        module = importlib.util.module_from_spec(spec)
        exec(aa, module.__dict__)
        return module
    except Exception as e:
        print(f"error load 'infrastructure module'")

def loader_provider(**constants):
    adapter = constants['adapter'] if 'adapter' in constants else ''
    service = constants['service'] if 'service' in constants else ''
    payload = constants['payload'] if 'payload' in constants else ''
    if service not in di:
        di[service] = lambda di: list([])
    req = js.XMLHttpRequest.new()
    req.open("GET", f"infrastructure/{service}/{adapter}.py", False)
    req.send()
    try:
        spec = importlib.util.spec_from_loader(adapter, loader=None)
        module = importlib.util.module_from_spec(spec)
        exec(req.response, module.__dict__)
        provider = getattr(module,'adapter')
        di[service].append(provider(config=payload))
    except Exception as e:
        print(f"error load 'infrastructure.{service}.{adapter}'")

def get_var(accessor_string,input_dict):
          """Gets data from a dictionary using a dotted accessor-string"""
          current_data = input_dict
          for chunk in accessor_string.split('.'):
              if type([]) == type(current_data):
                current_data = current_data[int(chunk)]
              else:
                current_data = current_data.get(chunk, {})
          return current_data


if sys.platform != 'emscripten':
    def loader_manager(**constants):
        driver = importlib.import_module(constants['path'], package=None)
        provider = getattr(driver,constants['name'])
        ser = constants['provider'] 
        if ser not in di:
            di[ser] = lambda di: list([])
        di[constants['name']] = lambda _di: provider(providers=di[ser])

    def loader_driver(**constants):
        driver = importlib.import_module(constants['path'], package=None)
        provider = getattr(driver,constants['name'])
        di[constants['name']] = lambda _di: provider()

    def loader_provider(**constants):
        adapter = constants['adapter'] if 'adapter' in constants else ''
        service = constants['service'] if 'service' in constants else ''
        payload = constants['payload'] if 'payload' in constants else ''

        if service not in di:
            di[service] = lambda di: list([])
        driver = importlib.import_module(f"infrastructure.{service}.{adapter}", package=None)
        provider = getattr(driver,'adapter')
        di[service].append(provider(config=payload))
else:
    def loader_manager(**constants):
        area,service,adapter = constants['path'].split('.')

        if service not in di:
            di[service] = lambda di: list([])
        try:
            req = js.XMLHttpRequest.new()
            req.open("GET", f"{area}/{service}/{adapter}.py", False)
            req.send()

            req2 = js.XMLHttpRequest.new()
            req2.open("GET", f"framework/service/language.py", False)
            req2.send()

            spec2 = importlib.util.spec_from_loader('language', loader=None)
            module2 = importlib.util.module_from_spec(spec2)
            exec(req2.response, module2.__dict__)
            
            spec = importlib.util.spec_from_loader(adapter, loader=None)
            module = importlib.util.module_from_spec(spec)
            module.language = module2
            exec(req.response, module.__dict__)

            provider = getattr(module,adapter)
            ser = constants['provider'] 
            if ser not in di:
                di[ser] = lambda di: list([])
            
            
            di[constants['name']] = lambda _di: provider(providers=di[ser])
        except Exception as e:
            print(constants)
            print(f"error load 'infrastructure.{service}.{adapter}' {repr(e)}")
    

    def loader_provider(**constants):
        adapter = constants['adapter'] if 'adapter' in constants else ''
        service = constants['service'] if 'service' in constants else ''
        payload = constants['payload'] if 'payload' in constants else ''
        area = constants['area'] if 'area' in constants else ''
        if service not in di:
            di[service] = lambda di: list([])
        try:
            req = js.XMLHttpRequest.new()
            req.open("GET", f"{area}/{service}/{adapter}.py", False)
            req.send()

            req2 = js.XMLHttpRequest.new()
            req2.open("GET", f"framework/service/language.py", False)
            req2.send()

            spec2 = importlib.util.spec_from_loader('language', loader=None)
            module2 = importlib.util.module_from_spec(spec2)
            exec(req2.response, module2.__dict__)
            
            spec = importlib.util.spec_from_loader(adapter, loader=None)
            module = importlib.util.module_from_spec(spec)
            module.language = module2
            exec(req.response, module.__dict__)

            provider = getattr(module,'adapter')
            di[service].append(provider(config=payload))
        except Exception as e:
            
            print(f"error load 'infrastructure.{service}.{adapter}' {repr(e)}")

def get_confi(**constants):
    jinjaEnv = Environment()
    if sys.platform != 'emscripten':
        with open('src/application/pyproject.toml', 'r') as f:
            text = f.read()
            template = jinjaEnv.from_string(text)
            content = template.render(constants)
            config = tomli.loads(content)
            return config
    else:
        req = js.XMLHttpRequest.new()
        req.open("GET", "application/pyproject.toml", False)
        req.send()
        text = str(req.response)
        template = jinjaEnv.from_string(text)
        content = template.render(constants)
        config = tomli.loads(content)
        return config

def get(domain,dictionary={}):
        output = None
        lista = [] 
        
        piec = domain.split('.')
        puntatore = dictionary.copy()
        for idx,key in enumerate(piec):
            if key.isnumeric():
                key = int(key)
            
            if key == '*':
                arr = get('.'.join(piec[:idx]),dictionary)
                for x in range(len(arr)):
                    aa = piec
                    aa[idx] = str(x)
                    nnnome = '.'.join(aa)
                    #print(nnnome)
                    lista.append(get(nnnome,dictionary))
                return lista

            if type(key) == type(10):
                if key > len(puntatore):
                    return None
            else:
                if not key in puntatore:
                    return None
            
            
            if idx == len(piec)-1:
                return puntatore[key]
            else:
                if len(puntatore) != 0:
                    puntatore = puntatore[key]

def put(domain,value,data=dict()):
        #print(domain)
        if type(domain) == type(list()):
            subdomain = domain[0].split('.')
        else:
            subdomain = domain.split('.')
        
        work = data.copy()
        puntatore = work
        
        for idx,key in enumerate(subdomain):
            #print(key,idx)
            if idx == len(subdomain)-1:
                #print(key,value)
                puntatore[key] = value
            else:
                if not key in puntatore:
                    if subdomain[idx+1].isnumeric():
                        puntatore[key] = []
                        puntatore = puntatore[key]
                    else:
                        if type(puntatore) == type([]):
                            #print(puntatore)
                            if 0 <= int(key) < len(puntatore):
                               puntatore = puntatore[int(key)]
                            else:
                                puntatore.insert(int(key), {})
                                puntatore = puntatore[int(key)]
                        else:
                            puntatore[key] = {}
                            puntatore = puntatore[key]

                else:
                    puntatore = puntatore[key]
        
        return work

def builder(schema,value=None,spread={}):
        output = dict({})
        order = ['type','model','iterable','default','regex']
        if type(schema) == type(tuple()):
            for row in schema:
                name = row['name'] if 'name' in row else '@'
                
                if 'model' in row:
                    name = row['model'][0]['name'] if 'name' in row['model'][0] and 'name' not in row else name
                a = builder(row,value,spread)
                output[name] = a
        elif type(schema) == type(''):
            if ':' in schema:
                splited = schema.split(':')
                #print(splited)
                model = importlib.import_module(f"application.{splited[0]}.{splited[1]}", package=None)
                output |= builder(getattr(model,splited[1]),value)
            else:
                model = importlib.import_module(f"application.model.{schema}", package=None)
                output |= builder(getattr(model,schema),value)
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

                            output[name] = builder(valore,passa,schema)
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
                                        a = builder(schema['type'],x)
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

def filter(self):
        pass

def first(self):
        pass

def last(self):
        pass

def keys(self):
        pass

def map(self):
        pass

def reduce(self):
        pass

def replace(self):
        pass

def slice(self):
        pass