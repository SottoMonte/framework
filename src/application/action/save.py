modules = {'flow':'framework.service.flow'}

@flow.asynchronous(managers=('messenger','storekeeper','presenter','tester'))
async def save(messenger,storekeeper,presenter,tester,**constants):
    identifier = constants.get('path','')
    model = constants.get('model','')
    target = constants.get('target','')
    component = await presenter.component(name=target.replace('block-editor-',''))
    value = component['editor'].getValue()

    #print(tester,'C-18')
    #response = await storekeeper.gather(repository='file',payload={'location':'SottoMonte/framework','path':identifier, 'content':value})
    
    state = await tester.unittest(value)

    print(state)

    if state['state']:
        '''response = await storekeeper.change(repository='file',payload={'location':'SottoMonte/framework','path':identifier, 'content':value})
        if response.get('state',False):
            await messenger.post(domain='success', message="Salvato")
        else:
            await messenger.post(domain='error', message="Errore non salvato")'''
        pass