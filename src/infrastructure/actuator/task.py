modules = {'flow': 'framework.service.flow',}

import sys

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

    @flow.asynchronous(outputs='transaction')
    async def load(self, *services, **constants):
        return await self.actuate(**constants | {'method': 'PUT'})

    async def actuate(self, **constants):
        print('request:',constants)
        headers = {
            "Authorization": f"{self.authorization} {self.token}",
            "Accept": self.accept,
        }
        location = constants.get('location','').replace('//','/')
        method = constants.get('method','')
        payload = constants.get('payload',{})
        url = f"{self.api_url}/{location}"

        #if payload and method == 'GET':
        #    url += '?' + urlencode(payload)
        
        ok = await backend(method,url,headers,payload)
        print('request:',constants,'output:',ok)
        return ok  
    
    @flow.asynchronous(outputs='transaction')
    async def activate(self,*services,**constants):
        return await self.actuate(**constants|{'method':'PUT'})

    @flow.asynchronous(outputs='transaction')
    async def deactivate(self,*services,**constants):
        pass

    @flow.asynchronous(outputs='transaction')
    async def calibrate(self,*services,**constants):
        pass

    @flow.asynchronous(outputs='transaction')
    async def status(self,*services,**constants):
        pass

    @flow.asynchronous(outputs='transaction')
    async def reset(self,*services,**constants):
        pass