modules = {'flow':'framework.service.flow'}

@flow.asynchronous(managers=('defender',))
async def login(defender,**constants):
    token = await defender.authenticate(ip='1111',identifier='asdasd',**constants)
    print(token,'login')
    if token:
        pass