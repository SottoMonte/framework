modules = {'flow':'framework.service.flow'}

@flow.asynchronous(managers=('messenger','storekeeper'))
async def create(messenger,storekeeper,**constants):
    #print('C18-',constants)
    name = constants.get('name','')
    if '.' not in name:
        name = f"{name}.py"
        constants['path'] += name+'/'
        constants['name'] = name
    response = await storekeeper.store(repository='file',payload=constants)

    if response.get('state',False):
        await messenger.post(domain='success', message=f"Creato {constants.get('path','')}/{constants.get('name','')}")
    else:
        await messenger.post(domain='error', message=f"Errore creazione {constants.get('path','')}/{constants.get('name','')}")