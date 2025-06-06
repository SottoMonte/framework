modules = {'flow':'framework.service.flow'}


@flow.asynchronous(managers=('messenger','presenter','executor'))
async def form(messenger,presenter,executor,**constants):
    target = constants.get('id','')
    action = constants.get('action','')
    form_data = {}
    # Ottieni il form e i dati
    
    form = await presenter.selector(id=target)
    print(type(form))
    elements = await presenter.get_attribute(widget=form[-1],field="elements")
    print('form:',form,target,elements)
    for input in elements:
        name = await presenter.get_attribute(widget=input,field="name")
        if name:
            if name.endswith('[]'):
                key = name[:-2]
                form_data.setdefault(key, []).append(input.value)
            else:
                form_data[name] = input.value
    print(form_data)

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

    print('items:', items,form_data)
    #await executor.act(action=action,**form_data|{'items':items})
    
    if not any(isinstance(v, list) for v in form_data.values()):
        print('Single item submission')
        await executor.act(action=action, **form_data)
    else:
        for item in items:
            await executor.act(action=action, **item)
    '''form_data = {}
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

    print('items:', items,form_data)
    #await executor.act(action=action,**form_data|{'items':items})
    
    if not any(isinstance(v, list) for v in form_data.values()):
        print('Single item submission')
        await executor.act(action=action, **form_data)
    else:
        for item in items:
            await executor.act(action=action, **item)'''



"""
import js
from js import document, fetch
@flow.asynchronous(managers=('messenger','presenter','executor'))
async def form(messenger,presenter,executor,**constants):
    target = constants.get('id','')
    action = constants.get('action','')
    # Ottieni il form e i dati
    
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

    print('items:', items,form_data)
    #await executor.act(action=action,**form_data|{'items':items})
    
    #for item in items:
    #    await executor.act(action=action,**item)

    if not any(isinstance(v, list) for v in form_data.values()):
        print('Single item submission')
        await executor.act(action=action, **form_data)
    else:
        for item in items:
            await executor.act(action=action, **item)"""

    