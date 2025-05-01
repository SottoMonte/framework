modules = {'flow':'framework.service.flow'}

@flow.asynchronous(managers=('messenger','storekeeper'))
async def delete(messenger,storekeeper,**constants):
    #print(constants)
    response = await storekeeper.remove(repository='file',payload=constants)

    if response.get('state',False):
        await messenger.post(domain='success', message=f"rimosso {constants.get('path','')}/{constants.get('name','')}")
    else:
        await messenger.post(domain='error', message=f"Errore rimuovi {constants.get('path','')}/{constants.get('name','')}")