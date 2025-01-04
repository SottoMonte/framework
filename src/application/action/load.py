flow = language.load_module(area="framework",service='service',adapter='flow')
import js
@flow.asynchronous(managers=('messenger','presenter','storekeeper'))
async def load(messenger,presenter,storekeeper,**constants):
    url = f'application/view/component/editor.xml'
    #print(constants)
    component = await presenter.component(name='ide')
    transaction = await storekeeper.gather(model="file",repo=component.get('repository'),file_path=constants.get('url',''))
    print(component)
    print(transaction)
    #text = await presenter.description(url=constants['url'])
    view = await presenter.builder(url=url,storekeeper=transaction)
    element = js.document.getElementById(constants['target'])
    element.appendChild(view)