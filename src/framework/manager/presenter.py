
class presenter():
    def __init__(self,**constants):
        self.providers = constants['providers']

    def __call__(self,**constants):
        if 'adapter' in constants:
            return di['presentation'][0].tree_view[constants['id']]
           # return await self.services[0].read(file=constants['url'])
        pass

    async def builder(self,**constants):
        b = language.last(self.providers)
        out = await b.builder(**constants)
        return out

    async def description(self,**constants):
        if 'module' in constants:
            return await di['persistence'].read(file=constants['module'])
        pass

    async def benchmark(self,**constants):
        if 'module' in constants:
            return await di['persistence'].read(file=constants['module'])
        pass

    async def effort(self,**constants):
        if 'module' in constants:
            return await di['persistence'].read(file=constants['module'])
        pass