from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import sys
import json
try:
    import supabase
except Exception as e:
    import js
    from js import supabase
    import pyodide

modules = {'flow': 'framework.service.flow'}

class adapter:
    def __init__(self, **config):
        """Inizializza il client Supabase con URL e chiave API."""
        self.config = config.get('config', {})
        #print(self.config)
        self.client = supabase.createClient(self.config['url'], self.config['key'])
        self.set_token(self.config.get('token', ''))

        js_code = f"""
  
        globalThis.supabaseClient = supabase.createClient("{self.config.get('url','')}", "{self.config.get('key','')}");

        console.log("✅ Supabase inizializzato!");
        """
        pyodide.code.run_js(js_code)
        

    def set_token(self, token):
        """Imposta il token di autenticazione dell'utente."""
        self.token = token
        self.client.auth.session = {"access_token": token}  # Usa il token per autenticazione


    async def query(self, **constants):
        print('BOOOOMq',constants,self.token,self.config)
        """
        Esegue una query su Supabase tramite supabase-js, con supporto per filtri e paginazione.
        """
        payload = json.dumps(constants.get('payload', {})) or "{}"
        method = constants.get('method', '')
        location = constants.get('location', '')
        filters = constants.get('filters', {})

        # Configura la paginazione
        page, per_page = filters.get('currentPage', 1), filters.get('perPage', 10)
        start, end = (page - 1) * per_page, page * per_page - 1  

        # Genera il codice JavaScript per la query
        js_code = f"""
        async function query() {{
            let query = supabaseClient.from("{location}");
            let response;

            const filters = {json.dumps(filters)};
            const payload = {payload};
            const method = "{method}";
            const location = "{location}";

            switch (method) {{
                case "GET":
                    response = await query.select("*");
                    break;
                case "POST":
                    response = await query.insert(payload);
                    break;
                case "PUT":
                    response = await query.update(payload);
                    break;
                case "DELETE":
                    response = await query.delete();
                    break;
                default:
                    return {{ state: false, error: "Invalid method", input: {{ method, payload, location, filters }} }};
            }}

            return response.error 
                ? {{ state: false, error: response.error.message, input: {{ method, payload, location, filters }} }}
                : {{ state: true, result: response.data, input: {{ method, payload, location, filters }} }};
        }}
        query();
        """
        test = await pyodide.code.run_js(js_code)
        print('BOOOOOMt',test.to_py())
        return test.to_py()
    
    async def query2(self, **constants):
        """Esegue una richiesta a Supabase utilizzando il token di autenticazione."""
        try:
            payload = constants.get('payload', {})
            method = constants.get('method', '')
            tt = constants.get('path', [])[0]

            print(tt)
            print(dir(supabase.fromTable('router')))
            filters = constants.get('filters', [])

        
            if method == 'GET':
                query = self.client.table(tt).select('*')
                for f in filters:
                    query = query.eq(f['field'], f['value'])
                response = query.execute()

            elif method == 'PUT':
                response = self.client.table(tt).update(payload).match(filters).execute()

            elif method == 'POST':
                response = self.client.table(tt).insert(payload).execute()

            elif method == 'DELETE':
                response = self.client.table(tt).delete().match(filters).execute()

            else:
                return {"state": False, "error": "Invalid method"}

           
            return {"state": bool(response.data), "result": response.data if response else "Request failed"}

        except Exception as e:
            print(f"Errore durante la richiesta: {e}")
            return {"state": False, "error": str(e)}

    @flow.asynchronous(outputs='transaction')
    async def create(self, **constants):
        """Inserisce un nuovo record nella tabella Supabase."""
        return await self.query(**constants | {'method': 'POST'})

    @flow.asynchronous(outputs='transaction')
    async def delete(self, **constants):
        """Elimina un record dalla tabella Supabase."""
        return await self.query(**constants | {'method': 'DELETE'})

    @flow.asynchronous(outputs='transaction')
    async def read(self, **constants):
        """Recupera i dati dalla tabella Supabase."""
        return await self.query(**constants | {'method': 'GET'})

    @flow.asynchronous(outputs='transaction')
    async def update(self, **constants):
        """Aggiorna un record nella tabella Supabase."""
        return await self.query(**constants | {'method': 'PUT'})