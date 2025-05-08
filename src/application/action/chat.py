modules = {'flow': 'framework.service.flow'}

@flow.asynchronous(managers=('messenger', 'presenter', 'storekeeper'))
async def chat(messenger, presenter,storekeeper, **constants):
    print(constants)
    component = await presenter.component(name='chat-ai')
    file = constants.get('file', '')

    payload = {'location':constants.get('location',''),'path':file}
    doc = ''
    files = []
    if 'src/application/view' in file:
        a = await storekeeper.gather(repository='file', payload=payload)
        files |= a.get('result',[])

    a = await storekeeper.gather(repository='file', payload=payload)
    files |= a.get('result',[])

    for file in files:
        doc += file['content']
    #print(a)
    constants.pop('file', None)
    constants.pop('location', None)
    #print(constants,'data')
    #print('component',component)
    component.setdefault('messenger',[]).append(constants)
    question = constants.get('message', '')
    ok = await messenger.post(domain='chat', message=f"Usa il seguente documento come base per rispondere alle domande dell'utente:\n\n{doc}"+question)
    #print(ok,question,'CHAT')