modules = {'flow': 'framework.service.flow'}

code_test = """
import unittest
import asyncio

# La tua classe repository modificata per usare self.language invece di language globale
modules = {'flow': 'framework.service.flow'}

class Test(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    def test_valid(self):
        self.assertTrue(False)
        #self.assertEqual(count, 2)"""

@flow.asynchronous(managers=('messenger', 'storekeeper'))
async def create(messenger, storekeeper, **constants):
    """
    Funzione asincrona per creare un file e gestire la comunicazione con i servizi di archiviazione e messaggistica.

    Args:
        messenger: Servizio di messaggistica per notifiche.
        storekeeper: Servizio di archiviazione per salvare i dati.
        **constants: Dizionario di parametri costanti.
    """
    # Recupera il nome dal dizionario `constants` o usa un valore predefinito
    name = constants.get('name', '')

    # Aggiunge l'estensione `.py` al nome se non è già presente
    if '.' not in name:
        name = f"{name}.py"
        constants['path'] += name + '/'
        constants['name'] = name

    # Se il file è un file Python ma non un file di test, crea anche un file di test
    if constants.get('name', '').endswith('.py') and not constants.get('name', '').endswith('.test.py'):
        test_file_name = constants['name'].replace('.py', '.test.py')
        test_file_payload = constants | {'name': test_file_name,'content': code_test}

        # Prova a salvare il file di test
        test_response = await storekeeper.store(repository='file', payload=test_file_payload)
        if test_response.get('state', False):
            await messenger.post(domain='success', message=f"Creato {constants.get('path', '')}{test_file_name}")
        else:
            await messenger.post(domain='error', message=f"Errore creazione {constants.get('path', '')}{test_file_name}")

    # Salva il file principale
    response = await storekeeper.store(repository='file', payload=constants)

    # Notifica il risultato del salvataggio
    if response.get('state', False):
        await messenger.post(domain='success', message=f"Creato {constants.get('path', '')}{constants.get('name', '')}")
    else:
        await messenger.post(domain='error', message=f"Errore creazione {constants.get('path', '')}{constants.get('name', '')}")