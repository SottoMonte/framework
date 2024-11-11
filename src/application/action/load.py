flow = language.load_module(area="framework",service='service',adapter='flow')
import js
@flow.async_function(ports=('messenger','presenter'))
async def load(messenger,presenter,**constants):
    url = f'application/view/component/block.xml'
    print(constants)
    text = await presenter.description(url=constants['url'])
    view = await presenter.builder(url=url,text=text)
    element = js.document.getElementById(constants['target'])
    element.appendChild(view)