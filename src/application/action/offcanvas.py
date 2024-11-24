flow = language.load_module(area="framework",service='service',adapter='flow')
import js
@flow.async_function(ports=('messenger','presenter'))
async def offcanvas(messenger,presenter,**constants):
    element = js.document.getElementById(constants['target'])
    match constants['act']:
        case 'open':
            element.setAttribute('data-bs-target',constants['id'])
            element.setAttribute('data-bs-toggle','offcanvas')
        case 'close':
            element.setAttribute('data-bs-dismiss','offcanvas')