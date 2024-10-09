import application.service.flow as flow

@flow.async_function(ports=('messenger','storekeeper'))
async def delete(messenger,storekeeper,**constants):
    payload = constants['payload']
    model = payload['model']
    identifier = payload['identifier']
    response = await storekeeper.pull(model=model, identifier=identifier)
    if response['state']: msg = "transaction completed"
    else: msg = "transaction failed"
    
    await messenger.post(name="log",value=f"Action on {model} {msg}")
    return response