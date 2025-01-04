import base64
import re


def build_tree_dict2(tree):
    """
    Costruisce una rappresentazione ad albero nidificata da una lista di percorsi.

    Args:
        tree (list): Lista di dizionari con chiavi "path", "type" e "sha".

    Returns:
        dict: Struttura ad albero nidificata che rappresenta i percorsi.
    """
    
    tree_dict = {}
    for item in tree:
        path_parts = item["path"].split("/")
        current = tree_dict
        for part in path_parts[:-1]:  # Itera fino al penultimo elemento
            current = current.setdefault(part, {})
        current[path_parts[-1]] = {"type": item["type"], "sha": item["sha"]}
    return tree_dict

def build_tree_dict(tree):
    """
    Costruisce una rappresentazione ad albero nidificata da una lista di percorsi,
    includendo il campo 'path' per ciascun nodo.

    Args:
        tree (list): Lista di dizionari con chiavi "path", "type" e "sha".

    Returns:
        dict: Struttura ad albero nidificata con percorsi completi.
    """
    def add_to_tree(tree, path_parts, sha, type_, parent_path="/"):
        """Funzione ricorsiva per aggiungere un percorso all'albero."""
        node_name = path_parts[0]
        current_path = f"{parent_path}{node_name}/"
        
        # Cerca il nodo nella lista dei figli
        for child in tree["children"]:
            if child["name"] == node_name:
                # Nodo trovato, continua la ricorsione
                if len(path_parts) > 1:
                    add_to_tree(child, path_parts[1:], sha, type_, current_path)
                return
        
        # Nodo non trovato, creane uno nuovo
        new_node = {
            "id": f"{parent_path.strip('/')}/{node_name}",
            "name": node_name,
            "path": current_path,
            "children": []
        }
        if len(path_parts) == 1:
            # Se è un nodo foglia, aggiungi informazioni sul tipo e lo sha
            new_node["type"] = type_
            new_node["sha"] = sha
        else:
            # Continua la ricorsione per i figli
            add_to_tree(new_node, path_parts[1:], sha, type_, current_path)
        
        # Aggiungi il nuovo nodo ai figli del nodo corrente
        tree["children"].append(new_node)
    # Nodo radice
    tree_dict = {
        'repository':re.search(r"https://api\.github\.com/repos/([^/]+/[^/]+)/", tree[0].get('url')).group(1),
        "id": "root",
        "name": "Root Node",
        "path": "",
        "children": []
    }
    
    for item in tree:
        path_parts = item["path"].split("/")
        add_to_tree(tree_dict, path_parts, item["sha"], item["type"])
    
    return tree_dict

def build_tree_dict3(tree):
    """
    Costruisce una rappresentazione ad albero nidificata da una lista di percorsi,
    convertendola in una struttura che segue il formato richiesto.

    Args:
        tree (list): Lista di dizionari con chiavi "path", "type" e "sha".

    Returns:
        dict: Struttura ad albero nidificata.
    """
    def add_to_tree(tree, path_parts, sha, type_, parent_id="root"):
        """Funzione ricorsiva per aggiungere un percorso all'albero."""
        node_name = path_parts[0]
        # Cerca il nodo nella lista dei figli
        for child in tree["children"]:
            if child["name"] == node_name:
                # Nodo trovato, continua la ricorsione
                if len(path_parts) > 1:
                    add_to_tree(child, path_parts[1:], sha, type_, child["id"])
                return
        
        # Nodo non trovato, creane uno nuovo
        new_node = {
            "id": f"{parent_id}_{node_name}",
            "name": node_name,
            "children": []
        }
        if len(path_parts) == 1:
            # Se è un nodo foglia, aggiungi informazioni sul tipo e lo sha
            new_node["type"] = type_
            new_node["sha"] = sha
        else:
            # Continua la ricorsione per i figli
            add_to_tree(new_node, path_parts[1:], sha, type_, new_node["id"])
        
        # Aggiungi il nuovo nodo ai figli del nodo corrente
        tree["children"].append(new_node)

    # Nodo radice
    tree_dict = {
        "id": "root",
        "name": "Root Node",
        "path":"/",
        "children": []
    }
    
    for item in tree:
        path_parts = item["path"].split("/")
        add_to_tree(tree_dict, path_parts, item["sha"], item["type"])
    
    return tree_dict

def decode(data):
    """
    Decodifica una stringa base64 in testo.

    Args:
        data (str): Stringa codificata in base64.

    Returns:
        str: Testo decodificato.
    """
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

#location = {'REPOSITORY':"repos/{repo}/contents/{file_path}"}
location = {'REPOSITORY':["repos/{repo}/git/trees/{tree_sha}?recursive=1","repos/{repo}","users/SottoMonte/repos"]}

values = {
    'tree':{'MODEL':build_tree_dict},
    'content':{'REPOSITORY':encode,'MODEL':decode},
}

mapper = {
    'name':{'REPOSITORY':'name'},
    'type':{'REPOSITORY':'type'},
    'content':{'REPOSITORY':'content'},
    'updated':{'REPOSITORY':'updated_at'},
    'language':{'REPOSITORY':'language'},
    'description':{'REPOSITORY':'description'},
    'visibility':{'REPOSITORY':'visibility'},
    'tree':{'REPOSITORY':'tree'},
}

async def create_payload(self,constants):
    payload = {
        "message": "Creating new file",
        "content": encode(constants.get('content',''))  # Content should be base64-encoded
    }
    return payload

async def delete_payload(self,constants):
    payload = {
        "message": "Deleting file",
        "sha": sha
    }
    return payload

async def write_payload(self,constants):
    payload = {
        "message": "Updating file",
        "content": base64.b64encode(constants.get('content','').encode()).decode(),
        "sha": sha
    }
    return payload

async def tree_payload(self,constants):
    repo = constants.get('repo','')
    branch = 'main'
    # Ottieni lo SHA del branch
    branch_url = f"{self.api_url}/repos/{repo}/branches/{branch}"
    branch_data = await self.query(method='GET',url=branch_url)
    tree_sha = branch_data['result']["commit"]["commit"]["tree"]["sha"]

    return {'tree_sha':tree_sha}

async def get(self,constants):
    payload = {
        "sort": constants.get("sortField", "full_name"),
        "direction": constants.get("sortDirection", "asc"),
        "per_page": constants.get("pageRows", "10"),
        "page": constants.get("pageCurrent", "1"),
    }
    return payload

payloads = {
    'create':create_payload,
    'delete':delete_payload,
    'update':write_payload,
    'read':get,
    'view':tree_payload
}