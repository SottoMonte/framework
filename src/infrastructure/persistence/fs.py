import framework.port.persistence as persistence
import framework.service.flow as flow
import os
import aiofiles

# File System (FS)

class adapter(persistence.port):

    def __init__(self,**constants):
        self.config = constants['config']

    async def query(self,**constants):
        pass

    @flow.async_function(ports=('storekeeper',))
    async def read(self,storekeeper,**constants):
        try:
            async with aiofiles.open(constants['file'], mode="r") as file:
                content = await file.read()
                return storekeeper.builder('transaction',{'state': True,'action':'read','result':dict({'file':content})})
        except FileNotFoundError:
            return storekeeper.builder('transaction',{'state': False,'action':'read'})

    @flow.async_function(ports=('storekeeper',))
    async def create(self,**constants):
        pass

    @flow.async_function(ports=('storekeeper',))
    async def delete(self,**constants):
        pass

    @flow.async_function(ports=('storekeeper',))
    async def write(self,**constants):
        try:
            async with aiofiles.open(constants['file'], mode="r") as file:
                content = await file.read()
                return content
        except FileNotFoundError:
            return "File non trovato."

    async def tree(self,**constants):
        # restituisci 
        albero = []
        for elemento in os.listdir(constants['path']):
            percorso_completo = os.path.join(constants['path'], elemento)
            if os.path.isdir(percorso_completo):
                # Ricorsione per le sottodirectory
                #print(percorso_completo)
                # print(percorso_completo)
                fs_tree = await self.tree(path=percorso_completo)
                albero.append(('dir',percorso_completo,elemento,fs_tree))
            else:
                albero.append(('file',percorso_completo,elemento))
        return tuple(albero)