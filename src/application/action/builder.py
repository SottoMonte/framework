flow = language.load_module(area="framework",service='service',adapter='flow')
import js
@flow.async_function(ports=('messenger','presenter'))
async def builder(messenger,presenter,**constants):
    url = f'application/view/component/{constants["component"]}.xml'
    view = await presenter.builder(url=url)
    element = js.document.getElementById(constants['target'])
    element.appendChild(view)