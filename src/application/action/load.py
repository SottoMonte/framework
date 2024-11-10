flow = language.load_module(area="framework",service='service',adapter='flow')
import js
@flow.async_function(ports=('messenger','presenter'))
async def load(messenger,presenter,**constants):
    url = f'application/view/component/block.xml'
    view = await presenter.builder(url=url)
    element = js.document.getElementById(language.last(constants['args']))
    element.appendChild(view)