# Import
import sys
import asyncio

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
    run = loader_provider(service='service',adapter='run') 
else:
    sys.path.insert(1, '../accent/src')
    import framework.service.run as run


if __name__ == "__main__":
    run.application(args=sys.argv)
    