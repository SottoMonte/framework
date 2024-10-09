#@flow.async_function(ports=('messenger','storekeeper'))
async def gather(messenger,storekeeper,**constants):
    payload = constants['payload']
    model = payload['model']
    response = await storekeeper.get(**payload)
    return response