modules = {'flow': 'framework.service.flow'}

@flow.asynchronous(managers=('messenger', 'storekeeper'),)
async def note(messenger, storekeeper, **constants):
    print(f"Note: {constants}")
    '''response = await storekeeper.store(repository='notes', payload=constants)

    # Notifica il risultato del salvataggio
    if response.get('state', False):
        await messenger.post(domain='success', message=f"Creato {constants.get('path', '')}{constants.get('name', '')}")
    else:
        await messenger.post(domain='error', message=f"Errore creazione {constants.get('path', '')}{constants.get('name', '')}")'''