#import application.port.language as language
from collections import OrderedDict


from kink import di
import importlib
import tomli
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
            
def load_module(**c):
    if sys.platform == 'emscripten':
        return loader_provider_test(**c)
    else:
        return ttt(**c)

async def get_module(path,lang):
    #response = js.fetch(f'application/action/{act}.py',{'method':'GET'})
    response = js.fetch(path,{'method':'GET'})
    file = await response
    aa = await file.text()
    
    neepath = path.replace('.py','')
    nettt = neepath.split('/')
    spec = importlib.util.spec_from_loader(last(nettt), loader=None)
    module = importlib.util.module_from_spec(spec)
    setattr(module,'language',lang)
    #print(aa,module.__dict__)
    exec(aa, module.__dict__)
    return module
    try:
        pass
    except Exception as e:
        print(f"error load 'infrastructure module'",str(e))

def get_module_os(path, lang):
    try:
        # Apriamo il file per la lettura
        with open(path, 'r') as file:
            aa = file.read()  # Leggi il contenuto del file

        # Rimuoviamo l'estensione .py
        nettt = path.split('/')
        module_name = last(nettt).replace('.py','')
        # Otteniamo il nome del modulo dall'ultima parte del percorso

        # Creiamo il modulo dinamicamente
        spec = importlib.util.spec_from_loader(module_name, loader=None)
        module = importlib.util.module_from_spec(spec)

        # Aggiungiamo l'attributo 'language' al modulo
        setattr(module, 'language', lang)

        # Eseguiamo il codice Python contenuto nel file
        exec(aa, module.__dict__)

        return module
    except Exception as e:
        print(f"Error loading 'infrastructure module': {str(e)}")

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
    def loader_provider_test(**constants):
        pass

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
    import js
    def loader_provider_test(**constants):

        
        adapter = constants['adapter'] if 'adapter' in constants else ''
        service = constants['service'] if 'service' in constants else ''
        payload = constants['payload'] if 'payload' in constants else ''
        area = constants['area'] if 'area' in constants else 'application'
            
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

def builderOld(schema,value=None,spread={},mode='full'):
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

async def builder(schema, value=None, spread={},mode='full',lang=None):
    def resolve_name(row):
        if 'model' in row:
            return row['model'][0].get('name', row.get('name', '@'))
        return row.get('name', '@')

    def import_model(path):
        module_name, attr_name = (path.split(':') if ':' in path else (f"model.{path}", path))
        model = importlib.import_module(f"application.{module_name}")
        return getattr(model, attr_name)

    if isinstance(schema, tuple):
        return {resolve_name(row): await builder(row, value, spread) for row in schema if mode != 'filtered' or (value and resolve_name(row) in value)}

    if isinstance(schema, str):
        module = await get_module(path=f'application/model/{schema}.py',lang=lang)
        model = getattr(module,schema)
        return await builder(model, value,spread,mode,lang)

    output = {}
    name = schema.get('name', spread.get('name', ''))
    if 'model' in schema:
        name = schema['model'][0].get('name', name)

    for field in ['type', 'model', 'iterable', 'default', 'regex']:
        if field not in schema:
            continue
        value_to_use = schema[field]
        match field:
            case 'iterable':
                output[name] = []
            case 'model':
                passa = value.get(name) if isinstance(value, dict) and name in value else value
                output[name] = builder(value_to_use, passa, schema)
            case 'type':
                output[name] = {'string': '', 'integer': 0, 'model': {}}.get(value_to_use, None)
            case 'default':
                ccc = value.get(name, value_to_use) if isinstance(value, dict) else value
                output[name] = ccc if isinstance(ccc, type(schema.get('type', None))) else value_to_use
                '''if isinstance(ccc, (list, dict)) and not isinstance(ccc, type(schema['type'])):
                    output[name] = [
                        builder(schema['type'], x) if isinstance(x, dict) else x
                        for x in ccc if isinstance(x, type(schema['type']))
                    ]
                else:
                    output[name] = ccc if isinstance(ccc, type(schema.get('type', None))) else value_to_use'''
            case 'regex':
                if name in output and not re.match(value_to_use, str(output[name])):
                    raise Exception(f"Regex not match {value_to_use}")

    return output[next(iter(output))] if len(output) == 1 else output


'''def translation(constants,values,keys,input='MODEL',output='MODEL'):
        
        out = dict()
        zwork = dict()

        for x in constants:
            #print(x,constants)
            zwork |= put(x,constants[x],zwork)
        #print(input,output,constants)
        for row in keys:
            if not input in row: dd = row['MODEL']
            else:dd = row[input]
            if not output in row: name = row['MODEL']
            else:name = row[output]

            trat = row['MODEL'] if dd not in row else dd

            if type(dd) == type([]):
                for x in dd:
                   valor = get(x,zwork)
                   #valor = [1,2,3] 
                   if valor != None:break
            else:valor = get(dd,zwork)
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
                out |= put(name,valor,out)
            
        
        return out'''

def translation2(constants, values, mapper, input='MODEL', output='MODEL'):
    try:
        """ Trasforma un set di costanti in un output mappato. """
        translated = {}
        for key in mapper:
            mapping = mapper[key]
            key_input = mapping.get(input, key)
            key_output = mapping.get(output, key)
            #print(constants)
            print(key,mapper,mapping,key_input,key_output,input,output)
            if type(constants) == type([]):
                lll = []
                for item in constants:
                    print(item)
                    value = get(key_input,item)
                    if key in values and output in values[key]:
                        value = values[key][output](value)
                        lll.append(value)
                    else:
                        lll.append(value)
                translated |= put(key_output,lll,translated)
            else:
                
                value = get(key_input,constants)
                #print(mapper,mapping,key_input,key_output,input,output,value)
                if key in values and output in values[key]:
                    value = values[key][output](value)
                translated |= put(key_output,value,translated)
        
    except Exception as e:
        print(f"Errore translation: {type(e).__name__}",e)
    return translated

def translation(constants, values, mapper, input='MODEL', output='MODEL'):
    try:
        """ Trasforma un set di costanti in un output mappato. """
        translated = {}
        for key in mapper:
            mapping = mapper[key]
            key_input = mapping.get(input, key)
            key_output = mapping.get(output, key)

            if key_input is None or key_output is None:
                raise ValueError(f"Invalid key mapping for key: {key}")

            if isinstance(constants, list):
                lll = []
                for item in constants:
                    value = get(key_input, item)
                    if key in values and output in values[key]:
                        if value is not None:
                            value = values[key][output](value)
                    else:
                        pass
                    lll.append(value)
                translated |= put(key_output, lll, translated)
            else:
                value = get(key_input, constants)

                if key in values and output in values[key]:
                    if value is not None:
                        value = values[key][output](value)           
                else:
                    pass
                translated |= put(key_output, value, translated)

    except Exception as e:
        print(f"Errore translation: {type(e).__name__}: {e}")
    return translated

def filter(self):
        pass

def first(self):
        pass

def last(iterable):
    return iterable[-1] if iterable else None

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