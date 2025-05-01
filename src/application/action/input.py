import js

modules = {'flow': 'framework.service.flow'}

@flow.asynchronous(managers=('messenger', 'presenter', 'storekeeper'),)
async def input(messenger, presenter, storekeeper, **constants):
    value = constants.get('value', '')
    inputs = constants.get('inputs', [])
    print(constants,'WOW22')
    for id in inputs:
        input = js.document.getElementById(id)
        input.value = value
    
    
    