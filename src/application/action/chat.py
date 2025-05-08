modules = {'flow': 'framework.service.flow'}

import os

@flow.asynchronous(managers=('messenger', 'presenter', 'storekeeper'))
async def chat(messenger, presenter, storekeeper, **constants):
    component = await presenter.component(name='chat-ai')
    file = constants.get('file', '')
    location = constants.get('location', '')
    message = constants.get('message', '')

    doc = ''
    paths = [file]
    directory = os.path.dirname(file.replace('src/application/', ''))
    path = 'src/application'
    for x in directory.split('/'):
        path = f"{path}/{x}"
        paths.append(path+f'/{x}.md')
    
    print('paths:', paths)

    for path in paths:
        payload = {'location': location, 'path': path}
        result = await storekeeper.gather(repository='file', payload=payload)
        doc += ''.join(f['content'] for f in result.get('result', []))

    component.setdefault('messenger', []).append(constants)
    await messenger.post(domain='chat', message=f"Usa il seguente documento come base per rispondere alle domande dell'utente:\n\n{doc} Utente msg:{message}")