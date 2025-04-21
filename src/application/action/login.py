modules = {'flow':'framework.service.flow'}

import js
from js import ace,console
@flow.asynchronous(managers=('defender',))
async def login(defender,**constants):
    token = await defender.authenticate(ip='1111',identifier='asdasd',**constants)

    print(token,'#')