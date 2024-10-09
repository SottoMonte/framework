import asyncio
import sys

if sys.platform == 'emscripten':
    import js
    import importlib.util
    def loader_provider(**constants):
        adapter = constants['adapter'] if 'adapter' in constants else ''
        service = constants['service'] if 'service' in constants else ''
        payload = constants['payload'] if 'payload' in constants else ''
            
        req = js.XMLHttpRequest.new()
        req.open("GET", f"http://localhost:8000/framework/{service}/{adapter}.py", False)
        req.send()
        try:
            spec = importlib.util.spec_from_loader(adapter, loader=None)
            module = importlib.util.module_from_spec(spec)
            exec(req.response, module.__dict__)
            return module
            #provider = getattr(module,'adapter')
            
        except Exception as e:
            print(f"error load 'infrastructure.{service}.{adapter}'")
    flow = loader_provider(service='service',adapter='flow')
    loader = loader_provider(service='service',adapter='loader')
    
else:
    import framework.service.flow as flow
    import framework.service.loader as loader

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