modules = {'flow':'framework.service.flow'}

import js

@flow.asynchronous(managers=('defender',))
async def login(defender,**constants):
    token = await defender.authenticate(ip='1111',identifier='asdasd',**constants)
    print(token,'login')
    if token:
        js.location.reload()
        pass