import os

def bootstrap_adapter() -> None:
        env = dict(os.environ)
        
        config = language.get_confi(**env)

        language.loader_manager(provider="message",name='messenger',path='framework.manager.messenger')
        language.loader_manager(provider="persistence",name='storekeeper',path='framework.manager.storekeeper')
        language.loader_manager(provider="presentation",name='presenter',path='framework.manager.presenter')
        language.loader_manager(provider="storekeeper",name='defender',path='framework.manager.defender')
        
        for module in ['presentation','persistence','message']:
            if module in config:
                for driver in config[module]:
                    setting = config[module][driver]
                    adapter = setting['adapter']
                    language.loader_provider(service=module,adapter=adapter,payload=setting|{'profile':driver}|{'project':config['project']})

    
    
    