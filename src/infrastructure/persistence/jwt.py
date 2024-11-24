import sys
if sys.platform == 'emscripten':
    import pyodide
    import json
    flow = language.load_module(area="framework",service='service',adapter='flow')
    persistence = language.load_module(area="framework",service='port',adapter='persistence')
else:
    import aiohttp
    import json
    import framework.port.persistence as persistence
    import framework.service.flow as flow
    import framework.service.language as language


class adapter(persistence.port):
    
    def __init__(self,**constants):
        self.config = constants['config']
        self.ssl = bool(self.config['ssl']) if 'ssl' in self.config else True
        self.url = self.config['url']
        if 'autologin' in self.config and self.config['autologin'] == 'true':
            self.token = self.login()

    async def query(self, *services, **constants):

        url = f"{self.url}/{constants['path']}"

        return url
    async def create(self, *services, **constants):
        pass
    async def delete(self, *services, **constants):
        pass
    async def read(self, *services, **constants):
        pass
    async def write(self, *services, **constants):
        pass
    async def tree(self):
        # Ottieni lo SHA dell'ultimo commit per il branch specificato
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"token {self.token}",
                "Accept": "application/vnd.github+json",
            }

            # Ottieni lo SHA del branch
            branch_url = f"{self.api_url}/branches/{self.branch}"
            async with session.get(branch_url, headers=headers) as branch_response:
                if branch_response.status != 200:
                    return {"state": False, "remark": "Failed to get branch details"}
                
                branch_data = await branch_response.json()
                tree_sha = branch_data["commit"]["commit"]["tree"]["sha"]

            # Ottieni la struttura dell'albero
            tree_url = f"{self.api_url}/git/trees/{tree_sha}?recursive=1"
            async with session.get(tree_url, headers=headers) as tree_response:
                if tree_response.status != 200:
                    return {"state": False, "remark": "Failed to get repository tree"}
                
                tree_data = await tree_response.json()
                return {"state": True, "tree": self.build_tree_dict(tree_data["tree"])}

    def build_tree_dict(self, tree):
        """
        Converte la lista piatta in un dizionario annidato.
        """
        tree_dict = {}
        for item in tree:
            parts = item["path"].split("/")
            current = tree_dict
            for part in parts[:-1]:
                current = current.setdefault(part, {})
            current[parts[-1]] = "file" if item["type"] == "blob" else {}

        return tree_dict