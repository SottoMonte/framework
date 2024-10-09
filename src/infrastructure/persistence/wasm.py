import js

class adapter():
    
    def __init__(self,**constants):
        
        self.config = constants['config']
    
    async def query(self, *services, **constants):
        pass

    #@flow.async_function(ports=('storekeeper','messenger'))
    async def read(self, **constants):
        print("tttt")
        resp = await js.fetch(constants['url'])
        print(resp.content)
        return resp.content

    #@flow.async_function(ports=('storekeeper','messenger'))
    async def create(self, storekeeper, messenger, **constants):
        
        s = {'method': "POST",}
        resp = await js.fetch(constants['url'],s)
        
        return resp.content

    #@flow.async_function(ports=('storekeeper',))
    async def delete(self, storekeeper, **constants):
        pass

    #@flow.async_function(ports=('storekeeper',))
    async def write(self, storekeeper, **constants):
        pass

    async def tree(self, *services, **constants):
        pass