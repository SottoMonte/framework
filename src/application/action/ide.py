flow = language.load_module(area="framework",service='service',adapter='flow')
import js
import asyncio
@flow.asynchronous(managers=('messenger','presenter','storekeeper'),)
async def ide(messenger,presenter,storekeeper,**constants):
    
    target = constants.get('id','')
    component = await presenter.component(name=target)
    #print('target',target)
    
    for key in constants:
        component[key] = constants[key]

    if 'loading' not in component:
        component |= await language.builder('ide',constants,{},'full',language)
    
    
    view = await presenter.builder(url=component.get('view'),component=component)

                
    element = js.document.getElementById(target)

    element.innerHTML = ''
    element.appendChild(view)