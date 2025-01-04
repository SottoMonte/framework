flow = language.load_module(area="framework",service='service',adapter='flow')
import js
from js import document, fetch
@flow.asynchronous(managers=('messenger','presenter','executor'))
async def form(messenger,presenter,executor,**constants):
    target = constants.get('id','')
    action = constants.get('action','')
    # Ottieni il form e i dati
    form = js.document.getElementById(target)
    print('form:',form,target)
    form_data = {input.name: input.value for input in form.elements if input.name}
    print('form_data:',form_data,executor)
    await executor.act(action=action,**form_data)

    