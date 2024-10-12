#import application.port.language as language
from collections import OrderedDict

import importlib
from kink import di

def get_var(accessor_string,input_dict):
          """Gets data from a dictionary using a dotted accessor-string"""
          current_data = input_dict
          for chunk in accessor_string.split('.'):
              if type([]) == type(current_data):
                current_data = current_data[int(chunk)]
              else:
                current_data = current_data.get(chunk, {})
          return current_data

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