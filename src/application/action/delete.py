flow = language.load_module(area="framework",service='service',adapter='flow')

@flow.asynchronous(managers=('messenger','storekeeper'))
async def delete(messenger,storekeeper,**constants):
    print(constants)
    response = await storekeeper.erase(**constants)