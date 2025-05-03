import sys
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

modules = {'flow': 'framework.service.flow',}

if sys.platform == 'emscripten':
    import pyodide
    import json

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
            return {"state": False, "result":[],"remark": f"Request failed with status {response.status}"}
                
else:
    import aiohttp
    import json

    #@flow.asynchronous
    async def backend(method,url,headers,payload):
        async with aiohttp.ClientSession() as session:
            async with session.request(method=method, url=url, headers=headers, json=payload) as response:
                data = await response.json()
                if response.status in [200, 201]:
                    
                    
                    return {"state": True, "result": data}
                else:
                    return {"state": False, "remark": f"Request failed with status {response.status}", "result":data}

class adapter():
    
    def __init__(self, **constants):
        self.config = constants['config']
        self.api_url = self.config.get('url','')
        self.token = self.config.get('token','')
        self.authorization = self.config.get('authorization','token ')
        self.accept = self.config.get('accept','application/vnd.github+json')

    async def request(self, **constants):
        headers = {
            "Authorization": f"{self.authorization.strip()} {self.token.strip()}",
            "Accept": self.accept,
            "Content-Type": self.accept,
        }
        location = constants.get('location','')
        method = constants.get('method','')
        payload = constants.get('payload',{
            "model": "deepseek/deepseek-chat-v3-0324:free",
            "messages": [
            {
                "role": "user",
                "content": "What is the meaning of life?"
            }
            ],
            
        })
        url = f"{self.api_url}"

        #if payload and method == 'GET':
        #    url += '?' + urlencode(payload)
        print(f"DEBUG - URL: {url}")
        print(f"DEBUG - Headers: {headers}")
        print(f"DEBUG - Payload: {payload}")
        ok = await backend(method,url,headers,payload)
        print('request:',constants,'output:',ok)
        exit(1)
        return ok
        
    @flow.asynchronous(outputs='transaction')
    async def post(self, **constants):
        return await self.request(**constants|{'method':'POST'})

    @flow.asynchronous(outputs='transaction')
    async def read(self, **constants):
        pass
        #return await self.request(**constants|{'method':'GET'})
    

