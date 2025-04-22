import base64
import re

modules = {'factory': 'framework.service.factory','flow': 'framework.service.flow'}

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

@flow.asynchronous(managers=('storekeeper',))
async def view(storekeeper,**constants):
    repo = constants.get('repo','framework')
    branch = 'main'
    payload = constants.get('payload',{})
    #payload |= {'name':repo,'branch':branch,'owner':'SottoMonte'}
    payload |= {'branch':branch,}

    
    branch_data = await storekeeper.gather(**constants|{'payload':payload})
    payload |= {'sha':branch_data.get('result')[0].get('sha')}
    payload.pop('branch')
    
    return payload

repository = factory.repository(
    location = {'GITHUB':[
        "repos/{owner}/{name}/git/trees/{sha}?recursive=1",
        "repos/{owner}/{name}/branches/{branch}",
        "repos/{owner}/{name}",
        "orgs/{owner}/repos",
        "user/repos?per_page={perPage}&page={currentPage}",
        "user/repos",
    ]},
    model = 'repository',
    values = {
        'tree':{'MODEL':build_tree_dict},
        #'content':{'REPOSITORY':encode,'MODEL':decode},
    },
    mapper = {
        'sha':{'GITHUB':'commit.commit.tree.sha'},
        'name':{'GITHUB':'name'},
        'branch':{'GITHUB':'branch'},
        'owner':{'GITHUB':'owner'},
        'type':{'REPOSITORY':'type'},
        'content':{'REPOSITORY':'content'},
        'updated':{'REPOSITORY':'updated_at'},
        'language':{'REPOSITORY':'language'},
        'description':{'REPOSITORY':'description'},
        'visibility':{'REPOSITORY':'visibility'},
        'tree':{'GITHUB':'tree'},
    },
    payloads = {
    #'create':create_payload,
    #'delete':delete_payload,
    #'update':write_payload,
        #'read':view,
        'view':view,
    }
)