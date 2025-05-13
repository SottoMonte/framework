
class presenter():
    def __init__(self,**constants):
        self.providers = constants['providers']

    def __call__(self,**constants):
        if 'adapter' in constants:
            return di['presentation'][0].tree_view[constants['id']]
           # return await self.services[0].read(file=constants['url'])
        pass

    async def builder(self,**constants):
        print('qui',constants)
        b = language.last(self.providers)
        out = await b.builder(**constants)
        return out

    def info(self,**constants):
        print('ok')

    async def description(self,**constants):
        b = language.last(self.providers)
        out = await b.host(constants)
        return out

    async def component(self,**constants):
        name = constants.get('name','')
        return self.providers[0].components[name]
    
    async def DOM(self,**constants):
        id = constants.get('id','')
        dom = self.providers[0].document
        if 'id' in constants:
            return dom.getElementById(id)
        
    async def rebuild(self,**constants):
        provider = language.last(self.providers)
        await provider.rebuild(constants.get('id',''),constants.get('view',''),**constants.get('data',dict()))


    async def benchmark(self,**constants):
        if 'module' in constants:
            return await di['persistence'].read(file=constants['module'])
        pass

    async def effort(self,**constants):
        if 'module' in constants:
            return await di['persistence'].read(file=constants['module'])
        pass