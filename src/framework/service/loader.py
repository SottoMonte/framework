from kink import di
import importlib
import tomli
import js
import sys
# pass le configurazioni qui
if sys.platform != 'emscripten':
    def loader_manager(**constants):
        driver = importlib.import_module(constants['path'], package=None)
        provider = getattr(driver,constants['name'])
        ser = constants['provider'] 
        if ser not in di:
            di[ser] = lambda di: list([])
        di[constants['name']] = lambda _di: provider(providers=di[ser])

    def loader_driver(**constants):
        driver = importlib.import_module(constants['path'], package=None)
        provider = getattr(driver,constants['name'])
        di[constants['name']] = lambda _di: provider()

    def loader_provider(**constants):
        adapter = constants['adapter'] if 'adapter' in constants else ''
        service = constants['service'] if 'service' in constants else ''
        payload = constants['payload'] if 'payload' in constants else ''

        if service not in di:
            di[service] = lambda di: list([])
        driver = importlib.import_module(f"infrastructure.{service}.{adapter}", package=None)
        provider = getattr(driver,'adapter')
        di[service].append(provider(config=payload))
else:
    def loader_manager(**constants):
        pass
    

    def loader_provider(**constants):
        adapter = constants['adapter'] if 'adapter' in constants else ''
        service = constants['service'] if 'service' in constants else ''
        payload = constants['payload'] if 'payload' in constants else ''
        if service not in di:
            di[service] = lambda di: list([])
        req = js.XMLHttpRequest.new()
        req.open("GET", f"infrastructure/{service}/{adapter}.py", False)
        req.send()
        try:
            spec = importlib.util.spec_from_loader(adapter, loader=None)
            module = importlib.util.module_from_spec(spec)
            exec(req.response, module.__dict__)
            provider = getattr(module,'adapter')
            di[service].append(provider(config=payload))
        except Exception as e:
            
            print(f"error load 'infrastructure.{service}.{adapter}'")
    

def bootstrap_adapter() -> None:
    try:
        if sys.platform != 'emscripten':
            with open('pyproject.toml', 'r') as f:
                config = tomli.loads(f.read())
        else:
            req = js.XMLHttpRequest.new()
            req.open("GET", "static/pyproject.toml", False)
            req.send()
            config = tomli.loads(str(req.response))

        loader_manager(provider="message",name='messenger',path='framework.manager.messenger')
        loader_manager(provider="persistence",name='storekeeper',path='framework.manager.storekeeper')
        loader_manager(provider="presentation",name='presenter',path='framework.manager.presenter')
        loader_manager(provider="storekeeper",name='defender',path='framework.manager.defender')
        
        for module in ['presentation','persistence','message']:
            if module in config:
                for driver in config[module]:
                    setting = config[module][driver]
                    adapter = setting['adapter']
                    loader_provider(service=module,adapter=adapter,payload=setting|{'profile':driver}|{'project':config['project']})

    except Exception as e:
        print("errore LOADER", repr(e))
        e_type = type(e).__name__
        e_file = e.__traceback__.tb_frame.f_code.co_filename
        e_line = e.__traceback__.tb_lineno

        e_message = str(e)

        print(f'exception type: {e_type}')

        print(f'exception filename: {e_file}')

        print(f'exception line number: {e_line}')

        print(f'exception message: {e_message}')
    
    