modules = {'flow':'framework.service.flow'}

@flow.asynchronous(managers=('messenger','storekeeper','presenter'))
async def save(messenger,storekeeper,presenter,**constants):
    identifier = constants.get('path','')
    model = constants.get('model','')
    target = constants.get('target','')
    component = await presenter.component(name=target.replace('block-editor-',''))
    value = component['editor'].getValue()
    
    response = await storekeeper.change(repository='file',payload={'location':'SottoMonte/framework','path':identifier, 'content':value})
    print(response,'save')
    if response.get('state',False):
        await messenger.post(domain='success', message="Salvato")
    else:
        await messenger.post(domain='error', message="Errore non salvato") 