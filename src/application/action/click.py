modules = {'flow':'framework.service.flow'}

@flow.asynchronous(managers=('messenger','storekeeper'))
async def click(messenger,storekeeper,**constants):
    pass