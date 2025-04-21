modules = {'flow':'framework.service.flow'}

@flow.asynchronous(managers=('defender',))
async def registration(defender,**constants):
    print("REGISTRATION")
    token = await defender.registration(ip='1111',identifier='asdasd',**constants)