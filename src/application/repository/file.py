modules = {'factory': 'framework.service.factory','flow': 'framework.service.flow'}

import base64

def decode(data):
    """
    Decodifica una stringa base64 in testo.

    Args:
        data (str): Stringa codificata in base64.

    Returns:
        str: Testo decodificato.
    """
    if not isinstance(data, str):
        raise TypeError("Il dato da decodificare deve essere una stringa.")

    return base64.b64decode(data).decode('utf-8')

def encode(data):
    """
    Codifica una stringa in base64.

    Args:
        data (str): Testo da codificare.

    Returns:
        str: Stringa codificata in base64.
    """
    if not isinstance(data, str):
        raise TypeError("Il dato da codificare deve essere una stringa.")
    return base64.b64encode(data.encode()).decode()

def rimuovi_ultimo_slash(stringa):
  """
  Rimuove l'ultimo slash di una stringa se presente.

  Args:
    stringa: La stringa da modificare.

  Returns:
    La stringa modificata, con l'ultimo slash rimosso, o la stringa originale se non c'è slash finale.
  """
  if stringa.endswith("/"):
    return stringa[:-1]
  else:
    return stringa

async def create_payload(**constants):
    payload = constants.get('payload',{})
    payload.pop('action')
    #payload.pop('location')
    payload |= {
        "message": "Creating new file",
        "content": encode(payload.get('content',''))  # Content should be base64-encoded
    }
    print(payload,'log')
    return payload

@flow.asynchronous(managers=('storekeeper',))
async def delete_payload(storekeeper,**constants):
    branch_data = await storekeeper.gather(**constants)
    sha = branch_data.get('result')[0].get('sha','')
    payload = {
        "message": "Deleting file",
        "sha": sha
    }
    return constants.get('payload')|payload

@flow.asynchronous(managers=('storekeeper',))
async def write_payload(storekeeper,**constants):
    branch_data = await storekeeper.gather(**constants)
    sha = branch_data.get('result')[0].get('sha','')
    payload = {
        "message": "Updating file",
        "content": base64.b64encode(constants.get('payload').get('content','').encode()).decode(),
        "sha": sha
    }
    return constants.get('payload')|payload

repository = factory.repository(
    location = {'GITHUB':[
       
       "repos/{payload.location}/contents/{payload.path}",
       "repos/{payload.location}/contents/{payload.path}/{payload.name}",
    ]},
    model = 'file',
    values = {
        'content':{'GITHUB':encode,'MODEL':decode},
        'path':{'GITHUB':rimuovi_ultimo_slash,'MODEL':rimuovi_ultimo_slash},
    },
    mapper = {
        'name':{'GITHUB':'name'},
        'type':{'GITHUB':'type'},
        'content':{'GITHUB':'content'},
    },
    payloads = {
        'create':create_payload,
        'delete':delete_payload,
        'update':write_payload,
    }
)