import framework.port.persistence as persistence
import aiohttp
import framework.service.flow as flow
#import urllib3
import json
#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class adapter(persistence.port):
    
    def __init__(self,**constants):
        self.config = constants['config']
        self.ssl = bool(self.config['ssl']) if 'ssl' in self.config else True
        self.url = self.config['url']
        if 'autologin' in self.config and self.config['autologin'] == 'true':
            self.token = self.login()

    def login(self):
        url = f"{self.config['url']}/Login"
        ddd = { "UserName":"manager", "Password":"s", "CompanyDB":"s",}
        response = requests.post(url, json = ddd,verify=False)
        
        if response.status_code == 200:
            return response.json()['SessionId']
        else:
            return ''
             
    def logout(self):
        url = f"{self.config['url']}/Login"
        head = {'Cookie':'B1SESSION='+self.token}
        response = requests.post(url, headers=head,verify=False)

        if response.status_code != 204:
            return None
        else:
            return response.json()

    async def query(self, *services, **constants):

        url = f"{self.url}/{constants['path']}"

        '''if 'identifier' in constants:
            url += f"('{constants['identifier']}')"
        else:
            row = constants['row'] if 'row' in constants else '10'
            page = str((int(constants['page'])-1)*int(row)) if 'page' in constants else str((int('1')-1)*int(row)) 
            url += f"?$top={row}&$skip={page}&$filter=CardType eq 'cCustomer'"
        
        if 'partition' or 'order' or 'filter' in constants:
            url += f"?"

        if 'order' in constants:
            url += "&$orderby=CardCode desc"
            

        if 'filter' in constants:
            url += f"$filter={constants['filter']['field']} eq '{constants['filter']['value']}'"'''

        return url

    @flow.async_function(ports=('storekeeper',))
    async def read(self, storekeeper, **constants):
        # passare tramite constant valore status code
        headers = {self.config['header_key']:self.config['header_value']+constants['token']}
        url = await self.query(**constants)
        
        async with aiohttp.ClientSession() as session:

            async with session.get(url, headers=headers,ssl=self.ssl) as response:
                if response.status != 200:
                    return storekeeper.builder('transaction',{'state': False,'action':'read','remark':'not found data'})
                else:
                    r = await response.json()
                    return storekeeper.builder('transaction',{'state': True,'action':'read','result':r})

        
    @flow.async_function(ports=('storekeeper',))
    async def create(self, storekeeper, **constants):
        head = {'Cookie':'B1SESSION='+self.token,'Content-type': 'application/json', 'Accept': 'text/plain'}
        if 'identifier' in constants:
            constants.pop('identifier')
        url = await self.query(**constants)

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=head,data=json.dumps(constants['value']),ssl=False) as response:
                if response.status == 201:
                    result = await response.json()
                    return storekeeper.builder('transaction',{'state': True,'action':'create','result':result})
                    
                else:
                    info = await response.json()
                    pp = {'url':url}
                    pp |= {k: constants[k] for k in set(list(constants.keys())) - set(['storekeeper'])}

                    return storekeeper.builder('transaction',{'state': False,'action':'create','result':info,'parameter':pp})

    @flow.async_function(ports=('storekeeper',))
    async def delete(self, storekeeper, **constants):
        head = {'Cookie':'B1SESSION='+self.token}
        url = await self.query(**constants)

        async with aiohttp.ClientSession() as session:

            async with session.delete(url, headers=head,ssl=False) as response:
                
                if response.status != 204:
                    info = await response.json()
                    pp = {'url':url}
                    print('====>>>',constants)
                    pp |= {k: constants[k] for k in set(list(constants.keys())) - set(['storekeeper'])}
                    return storekeeper.builder('transaction',{'state': False,'action':'delete','result':info,'parameter':pp})
                else:
                    return storekeeper.builder('transaction',{'state': True,'action':'delete'})

    async def write(self, *services, **constants):
        head = {'Cookie':'B1SESSION='+self.token}
        url = await self.query(**constants)
        response = requests.patch(url, headers=head,verify=False)
        
        if response.status_code != 204:
            return None
        else:
            return response.json()

    async def tree(self, *services, **constants):
        pass