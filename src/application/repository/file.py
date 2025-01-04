import base64
import ast

def build_code_tree(file_path):
    """
    Analizza un file Python e costruisce un albero di funzioni, classi, metodi e variabili.

    Args:
        file_path (str): Percorso al file Python da analizzare.

    Returns:
        dict: Struttura ad albero del codice.
    """
    class CodeTreeBuilder(ast.NodeVisitor):
        def __init__(self):
            self.tree = {"type": "module", "name": "root", "children": []}
            self.stack = [self.tree]

        def visit_FunctionDef(self, node):
            # Nodo funzione
            function_node = {
                "type": "function",
                "name": node.name,
                "lineno": node.lineno,
                "children": []
            }
            self.stack[-1]["children"].append(function_node)
            self.stack.append(function_node)
            self.generic_visit(node)
            self.stack.pop()

        def visit_AsyncFunctionDef(self, node):
            # Nodo funzione asincrona
            async_function_node = {
                "type": "async_function",
                "name": node.name,
                "lineno": node.lineno,
                "children": []
            }
            self.stack[-1]["children"].append(async_function_node)
            self.stack.append(async_function_node)
            self.generic_visit(node)
            self.stack.pop()

        def visit_ClassDef(self, node):
            # Nodo classe
            class_node = {
                "type": "class",
                "name": node.name,
                "lineno": node.lineno,
                "children": []
            }
            self.stack[-1]["children"].append(class_node)
            self.stack.append(class_node)
            self.generic_visit(node)
            self.stack.pop()

        def visit_Assign(self, node):
            # Nodo assegnazione variabile
            for target in node.targets:
                if isinstance(target, ast.Name):
                    var_node = {
                        "type": "variable",
                        "name": target.id,
                        "lineno": node.lineno
                    }
                    self.stack[-1]["children"].append(var_node)
            self.generic_visit(node)

        def visit_AnnAssign(self, node):
            # Nodo assegnazione con annotazione
            if isinstance(node.target, ast.Name):
                var_node = {
                    "type": "annotated_variable",
                    "name": node.target.id,
                    "lineno": node.lineno
                }
                self.stack[-1]["children"].append(var_node)
            self.generic_visit(node)

   
    source_code = decode(file_path)
    #print(source_code)
    # Parsing del codice sorgente
    parsed_tree = ast.parse(source_code)

    # Costruzione dell'albero
    builder = CodeTreeBuilder()
    builder.visit(parsed_tree)

    return builder.tree

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

location = {'REPOSITORY':["repos/{repo}/contents/{file_path}"]}

values = {
    'tree':{'MODEL':build_code_tree},
    'content':{'REPOSITORY':encode,'MODEL':decode},
}

mapper = {
    'identifier':{'REPOSITORY':'id'},
    'name':{'REPOSITORY':'name'},
    'owner':{'REPOSITORY':'owner.login'},
    'location':{'REPOSITORY':'html_url'},
    'type':{'REPOSITORY':'type'},
    'content':{'REPOSITORY':'content'},
    'tree':{'REPOSITORY':'content'},
}

async def create_repo(self,constants):
    payload = {
        "message": "Creating new file",
        "content": encode(constants.get('content',''))  # Content should be base64-encoded
    }
    return payload

async def delete(self,constants):
    constants.pop('payload')
    file = await self.read(**constants)
    
    sha = file['result']["sha"]
    print('sha:',sha)
    payload = {
        "message": "Deleting file",
        "sha": sha
    }
    return payload

async def update(self,constants):
    constants.pop('payload')
    file = await self.read(**constants)
    
    sha = file['result']["sha"]
    
    payload = {
        "message": "Updating file",
        "content": encode(constants.get('content','')),
        "sha": sha
    }
    return payload

payloads = {
    'create':create_repo,
    'delete':delete,
    'update':update,
}