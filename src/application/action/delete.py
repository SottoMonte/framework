modules = {'flow':'framework.service.flow'}

@flow.asynchronous(managers=('messenger','storekeeper'))
async def delete(messenger,storekeeper,**constants):
    print(constants)
    response = await storekeeper.erase(**constants)