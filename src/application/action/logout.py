modules = {'flow':'framework.service.flow'}

@flow.asynchronous(managers=('defender',))
async def logout(defender,**constants):
    print("logout test")
    await defender.logout(ip='1111',identifier='asdasd',**constants)