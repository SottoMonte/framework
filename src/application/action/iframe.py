import js
import asyncio

modules = {'flow': 'framework.service.flow'}

@flow.asynchronous(managers=('messenger', 'presenter', 'storekeeper'),)
async def iframe(messenger, presenter, storekeeper, **constants):
    target = constants.get('id', 'myIframe')  # ID dell'iframe
    iframe_url = constants.get('src', '')     # URL da caricare
    if 'target' in constants:
        target = constants['target']
        v = js.document.getElementById(target)
        iframe_url = v.value

    print(f"Updating iframe '{target}' to load: {iframe_url}")
    
    iframe_element = js.document.getElementById(target)
    iframe_element.src = iframe_url
    
    
    