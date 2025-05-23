modules = {'flow':'framework.service.flow'}

import js
from js import document, fetch
@flow.asynchronous(managers=('messenger','presenter','executor'))
async def form(messenger,presenter,executor,**constants):
    target = constants.get('id','')
    action = constants.get('action','')
    # Ottieni il form e i dati
    '''form = js.document.getElementById(target)
    print('form:',form,target)
    form_data = {input.name: input.value for input in form.elements if input.name}
    print('form_data:',form_data,executor)
    await executor.act(action=action,**form_data)'''
    form = js.document.getElementById(target)
    print('form:',form,target)
    form_data = {}
    for input in form.elements:
        if input.name:
            if input.name.endswith('[]'):
                key = input.name[:-2]
                form_data.setdefault(key, []).append(input.value)
            else:
                form_data[input.name] = input.value
    print('form_data:',form_data,executor)
    
    max_len = max((len(v) for v in form_data.values() if isinstance(v, list)), default=1)
    items = []
    # Cicla su ogni elemento da aggiornare
    for i in range(max_len):
        item = {}
        for key, value in form_data.items():
            if isinstance(value, list):
                item[key] = value[i] if i < len(value) else None
            else:
                item[key] = value
        items.append(item)

    print('items:', items)
    #await executor.act(action=action,**form_data|{'items':items})
    for item in items:
        await executor.act(action=action,**item)

    