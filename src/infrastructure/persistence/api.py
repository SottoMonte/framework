import sys
import re
from urllib.parse import urlencode, urlparse, urlunparse, parse_qs


def add_query_params(url, params):
    # Parsifica l'URL nei suoi componenti
    url_parts = urlparse(url)
    
    # Converte i parametri esistenti e i nuovi in un dizionario
    query_params = parse_qs(url_parts.query)
    query_params.update(params)
    
    # Codifica nuovamente i parametri come stringa
    new_query = urlencode(query_params, doseq=True)
    
    # Ricostruisce l'URL con i nuovi parametri
    new_url = urlunparse(url_parts._replace(query=new_query))
    return new_url


if sys.platform == 'emscripten':
    import pyodide
    import json
    flow = language.load_module(area="framework",service='service',adapter='flow')
    async def backend(method,url,headers,payload):
        match method:
            case 'GET':
                response = await pyodide.http.pyfetch(url, method=method, headers=headers)
            case _:
                if type(payload) == dict:
                    payload = json.dumps(payload)
                else:
                    payload = json.dumps({})
                response = await pyodide.http.pyfetch(url, method=method, headers=headers,body=payload)
        if response.status in [200, 201]:
            data = await response.json()
            print(data)
            return {"state": True, "result": data}
        else:
            return {"state": False, "remark": f"Request failed with status {response.status}"}
                
else:
    import aiohttp
    import json
    import framework.service.flow as flow
    import framework.service.language as language

    #@flow.asynchronous
    async def backend(method,url,headers,payload):
        async with aiohttp.ClientSession() as session:
            async with session.request(method=method, url=url, headers=headers, json=payload) as response:
                if response.status in [200, 201]:
                    data = await response.json()
                    
                    return {"state": True, "result": data}
                else:
                    return {"state": False, "remark": f"Request failed with status {response.status}"}

class adapter():
    
    def __init__(self, **constants):
        self.config = constants['config']
        self.api_url = self.config['url']
        self.token = self.config['token']
        self.authorization = self.config['authorization'] if 'authorization' in self.config else 'token '
        self.accept = self.config['accept'] if 'accept' in self.config else 'application/vnd.github+json'
    
    async def query(self, **constants):
        def can_format(template, data):
            """
            Verifica se una singola stringa `template` può essere formattata utilizzando le chiavi di un dizionario `data`.
            """
            try:
                placeholders = re.findall(r'\{(\w+)\}', template)
    
                # Controlla che tutti i placeholder siano presenti nelle chiavi del dizionario
                return all(key in data for key in placeholders)
            except Exception as e:
                print(f"Errore durante la verifica: {e}")
                return False
        def find_first_formattable_template(templates, data):
            """
            Trova il primo template nella lista che può essere formattato con il dizionario `data`.

            :param templates: Lista di stringhe che contengono i placeholder.
            :param data: Dizionario con le chiavi e i valori per il formato.
            :return: Il primo template formattabile o None se nessuno è valido.
            """
            for template in templates:
                if can_format(template, data):
                    return template
            return ''
        if 'payload' in constants:
            print(type(constants['payload']),'gggg')
            payload = constants['payload']
        else:
            payload = {}
        method = constants.get('method','')
        token = constants.get('token',self.token)
        headers = {
            "Authorization": f"{self.authorization} {token}",
            "Accept": f"{self.accept}",
        }
        templates = constants.get('path',[''])

        
        print(type(payload),'payload ---------->2',payload)
        # Verifica che tutti i placeholder siano presenti nel dizionario
        #path = template.format(**constants)
        template = find_first_formattable_template(templates, constants)
        path = template.format(**constants)
        url2 = f"{self.api_url}/{path}"
        url = constants.get('url',url2)

        if type(payload) == dict and method == 'GET':
            url = add_query_params(url,payload)
            print('url:',url)

        return await backend(method,url,headers,payload)

    async def engine(self, **constants):
        
        url = constants.get('url','')
        payload = constants.get('payload',{})
        method = constants.get('method','')
        headers = {
            "Authorization": f"{self.authorization} {self.token}",
            "Accept": f"{self.accept}",
        }
        return await backend(method,url,headers,payload)
        

    async def create(self, *services, **constants):
        print(constants)
        payload = constants.get('payload',None)
        if payload:
            payload = await payload(self,constants)
        return await self.query(**constants|{'method':'PUT','payload':payload})

    async def delete(self, *services, **constants):
        payload = constants.get('payload',None)
        if payload:
            payload = await payload(self,constants)
        return await self.query(**constants|{'method':'DELETE','payload':payload})

    async def read(self, *services, **constants):
        
        payload = constants.get('payload',None)
        if payload:
            print('payload:------------:',payload)
            payload = await payload(self,constants)
            
        return await self.query(**constants|{'method':'GET','payload':payload})

    async def update(self, *services, **constants):
        print(constants)
        payload = constants.get('payload',{})
        if payload:
            payload = await payload(self,constants)
            print(type(payload),'qui',payload)
        else:
            payload = {}
        gggg = constants|{'payload':payload}
        return await self.query(**gggg|{'method':'PUT'})

    async def view(self,**constants):
        
        payload = constants.get('payload',None)
        if payload:
            payload = await payload(self,constants)
        #payload=payload
        return await self.query(**constants|{'method':'GET'}|payload)