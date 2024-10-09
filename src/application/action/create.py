import application.service.flow as flow

@flow.async_function(ports=('messenger','storekeeper'))
async def create(messenger,storekeeper,**constants):
    payload = constants['payload']
    model = payload['model']
    value = payload['value']
    response = await storekeeper.put(model=model, identifier=value['identifier'], value=value)
    return response
    #print(constants,response)