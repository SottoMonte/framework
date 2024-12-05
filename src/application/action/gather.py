#gather()
flow = language.load_module(area="framework",service='service',adapter='flow')

@flow.async_function(ports=('messenger','storekeeper'))
async def gather(messenger,storekeeper,**constants):
    '''payload = constants['payload']
    model = payload['model']
    response = await storekeeper.get(**payload)
    return response'''
    response = await storekeeper.get(model="repository",repo="org/repo_name", branch="main")