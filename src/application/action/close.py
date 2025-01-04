flow = language.load_module(area="framework",service='service',adapter='flow')
import js
@flow.asynchronous(managers=('messenger','presenter'))
async def close(messenger,presenter,**constants):
    _ = await presenter.builder()
    print('ciao da close',constants)
    element = js.document.getElementById(constants['target'])
    element.remove()