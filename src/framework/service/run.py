import asyncio
import sys

flow = language.load_module(area="framework",service='service',adapter='flow')
loader = language.load_module(area="framework",service='service',adapter='loader')

loader.bootstrap_adapter()

@flow.function(ports=('presentation',))
def application(presentation=[],**constants):
    
    app = constants
    
    eventloop = asyncio.new_event_loop()
    asyncio.set_event_loop(eventloop)
    
    try:
        for x in presentation:
            x.loader(loop=eventloop)
        
        eventloop.run_forever()
    except Exception as e:
        print("errore generico",e)
    except KeyboardInterrupt:
        print("Ctrl + C")