import os
import sys

def bootstrap_adapter() -> None:
        env = dict(os.environ)
        
        if sys.platform == 'emscripten':
            import js
            cookies = {}
            for cookie in js.document.cookie.split(';'):
                if '=' in cookie:
                    key, value = cookie.split('=', 1)
                    cookies[key.strip()] = value
            #print(js.document.cookie,"<-----",cookies)
            config = language.get_confi(**env|cookies)
        else:
            config = language.get_confi(**env)

        language.loader_manager(provider="message",name='messenger',path='framework.manager.messenger')
        language.loader_manager(provider="persistence",name='storekeeper',path='framework.manager.storekeeper')
        language.loader_manager(provider="presentation",name='presenter',path='framework.manager.presenter')
        language.loader_manager(provider="authentication",name='defender',path='framework.manager.defender')
        language.loader_manager(provider="authentication",name='tester',path='framework.manager.tester')
        language.loader_manager(provider="authentication",name='executor',path='framework.manager.executor')
        
        for module in ['presentation','persistence','message','authentication']:
            if module in config:
                for driver in config[module]:
                    setting = config[module][driver]
                    adapter = setting['adapter']
                    language.loader_provider(area='infrastructure',service=module,adapter=adapter,payload=setting|{'profile':driver}|{'project':config['project']})

    
    
    