import application.service.flow as flow

@flow.async_function(ports=('messenger','storekeeper'))
async def update(messenger,storekeeper,**constants):
    payload = constants['payload']
    model = payload['model']
    value = payload['value']
    response = await storekeeper.alter(model=model, identifier=value['identifier'], value=value)
    if response['state']: msg = "transaction completed"
    else: msg = "transaction failed"
        
    await messenger.post(name="log",value=f"Action on {model} {msg}")
    #print(constants,response)