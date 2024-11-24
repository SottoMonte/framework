

try:
    #import framework.port.presentation as presentation
    import framework.service.flow as flow

    from starlette.applications import Starlette
    from starlette.requests import Request
    from starlette.responses import JSONResponse,HTMLResponse,RedirectResponse
    from starlette.routing import Route,Mount,WebSocketRoute
    from starlette.middleware import Middleware
    from starlette.websockets import WebSocket
    #from starlette.middleware.cors import CORSMiddleware
    from starlette.middleware.sessions import SessionMiddleware
    from starlette.staticfiles import StaticFiles
    from jinja2 import Environment, select_autoescape,FileSystemLoader,BaseLoader,ChoiceLoader,Template

    import untangle

    import os
    import uuid
    #import uvicorn
    from uvicorn import Config, Server

    # Auth 
    #from starlette.middleware.sessions import SessionMiddleware
    from datetime import timedelta
    import secrets
    #from starlette_login.middleware import AuthenticationMiddleware

    #
    from starlette.requests import HTTPConnection
    from starlette.types import ASGIApp, Message, Receive, Scope, Send

    from starlette.datastructures import MutableHeaders
    import http.cookies
    import markupsafe
    from bs4 import BeautifulSoup
except Exception as e:
    import markupsafe
    from bs4 import BeautifulSoup
    flow = language.load_module(area="framework",service='service',adapter='flow')
    starlette = None
    import untangle
    print("errore generico",e)

#presentation.presentation
class adapter():

    @flow.function(ports=('defender',))
    def __init__(self,defender,**constants):
        self.config = constants['config']
        self.views = dict({})
        cwd = os.getcwd()

        routes=[
            Mount('/static', app=StaticFiles(directory=f'{cwd}/public/'), name="static"),
            Mount('/framework', app=StaticFiles(directory=f'{cwd}/src/framework'), name="y"),
            Mount('/application', app=StaticFiles(directory=f'{cwd}/src/application'), name="z"),
            Mount('/infrastructure', app=StaticFiles(directory=f'{cwd}/src/infrastructure'), name="x"),
            #WebSocketRoute("/ws", self.websocket, name="ws"),
        ]

        self.mount_route(routes,self.config['routes'])

        middleware = [
            Middleware(SessionMiddleware, session_cookie="session_state",secret_key=self.config['project']['key']),
            #Middleware(AuthorizationMiddleware, manager=defender)
        ]

        self.app = Starlette(debug=True,routes=routes,middleware=middleware)

    def loader(self, *services, **constants):
        try:
            fs_loader = FileSystemLoader("src/application/view/layout/")
            #http_loader = MyLoader()
            #choice_loader = ChoiceLoader([fs_loader, http_loader])
            self.env = Environment(loader=fs_loader,autoescape=select_autoescape(["html", "xml"]))
            loop=constants['loop']
            config = Config(app=self.app, loop=loop,host=self.config['host'], port=int(self.config['port']),use_colors=True,reload=True)
            server = Server(config)
            loop.create_task(server.serve())
        except Exception as e:
            print("errore generico",e)

    async def host(self,constants):
        f = open('src/'+constants['url'], "r")
        text = f.read()
        return text

    async def builder(self,**constants):
        text = await self.host(constants)
        template = self.env.from_string(text)
        content = template.render(constants)
        xml = untangle.parse(content)
        view = await self.mount_view(xml.children[0],constants)
        return view
        
    @flow.async_function(ports=('defender',))
    async def logout(self,request,defender) -> None:
        assert request.scope.get("app") is not None, "Invalid Starlette app"
        request.session.clear()
        response = RedirectResponse('/', status_code=303)
        response.delete_cookie("session_token")
        return response

    @flow.async_function(ports=('storekeeper','defender',))
    async def login(self,request, storekeeper, defender) -> None:
        match request.method:
            case 'GET':
                query = dict(request.query_params)
                session_identifier = request.cookies.get('session_identifier', secrets.token_urlsafe(16))
                #session_token = request.cookies.get('session_token', 'Cookie not found')
                token = await defender.authenticate(identifier=session_identifier,**query)
                
                transaction = await storekeeper.get(model="user",token=token)
                if transaction['state']:
                    request.session.update(transaction['result'])
                
                response = RedirectResponse('/', status_code=303)
                if 'session_identifier' not in request.cookies:
                    response.set_cookie(key='session_identifier', value=session_identifier, max_age=3600)
                response.set_cookie(key='session_token', value=token, max_age=3600)
                return response
            case 'POST':
                credential = await request.form()
                credential = dict(credential)
                session_identifier = request.cookies.get('session_identifier', secrets.token_urlsafe(16))
                #session_token = request.cookies.get('session_token', 'Cookie not found')
                token = await defender.authenticate(identifier=session_identifier,**credential)
                
                transaction = await storekeeper.get(model="user",token=token)
                
                if transaction['state']:
                    request.session.update(transaction['result'])
                
                response = RedirectResponse('/', status_code=303)
                if 'session_identifier' not in request.cookies:
                    response.set_cookie(key='session_identifier', value=session_identifier, max_age=3600)
                response.set_cookie(key='session_token', value=token, max_age=3600)
                return response

    async def websocket(self,websocket):
        
        await websocket.accept()
        # Process incoming messages
        while True:
            mesg = await websocket.receive_text()
            await websocket.send_text(mesg.replace("Client", "Server"))
        await websocket.close()
    

    @flow.async_function(ports=('storekeeper',))
    async def model(self,request,storekeeper,**constants):
        print(request.url.path)
        #form = await request.form()
        #code="C00011615",name="Marco Rullo",firstName="Marco",lastName="Rullo",gender='f'
        #print(dict(form))
        #b = await storekeeper.get(model='client',identifier=form['identifier'])
        a = await storekeeper.get(name='router',model='router',identifier='04B4FE83486D',value={'model': 'router','anno':400})
        return JSONResponse(a)
    
    @flow.async_function(ports=('storekeeper','messenger'))
    async def action(self, request, storekeeper, messenger, **constants):
        #print(request.cookies.get('user'))
        match request.method:
            case 'GET':
                query = dict(request.query_params)
                #await messenger.post(identifier=id,name=request.url.path[1:],value=dict(query))
                #data = await messenger.get(identifier=id,name=request.url.path[1:],value=dict(query))
                import application.action.gather as gather
                
                data = await gather.gather(messenger,storekeeper,model=query['model'],payload=query)
                return JSONResponse(data)
                
            case 'POST':
                form = await request.form()
                data = dict(form)
                
                request.scope["user"] = data
                #await messenger.post(name=request.url.path[1:],value={'model':data['model'],'value':data})
                return RedirectResponse('/', status_code=303)

    async def view(self,request):
        html = await self.builder(url=self.views[request.url.path])
        layout = 'application/view/layout/base.html'
        file = await self.host({'url':layout})
        template = self.env.from_string(file)
        content = template.render()
        content = content.replace('<!-- Body -->',html)
        return HTMLResponse(content)
    
    def code(self,tag,attr,inner=[]):
        att = ''
        html = ''
        for key in attr:
            att += f' {key}="{attr[key]}"'
        if type(inner) == type([]):
            for item in inner:
                html += item
            return f'<{tag} {att} >{html}</{tag}>'
        elif  type(inner) == type(''):
            return f'<{tag} {att} >{inner}</{tag}>'
        else:
            return f'<{tag} {att} />'

    def att(self,element,attributes):
        pass

    def convert(self, html):
        # Parsing del codice HTML con BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        # Mappatura dei tipi di elementi da convertire
        element_map = {
            'Layout': {'tags': ['div'], 'attrs': {}},
            'Text': {'tags': ['p'], 'attrs': {}},
            'Action': {'tags': ['a', 'form'], 'attrs': {'href': 'route'}},
            'Graph': {'tags': ['img','i'], 'attrs': {'class': 'icon'}},
            'Group': {'tags': ['li','ul'], 'attrs': {}},
        }
        
        # Iterare attraverso gli elementi da mappare
        for category, settings in element_map.items():
            # Estrarre i tag da modificare
            tags_to_process = settings['tags']
            attribute_map = settings['attrs']
            
            # Per ogni tag definito nella mappatura
            for tag in tags_to_process:
                for tag_element in soup.find_all(tag):
                    # Cambiare il nome del tag
                    tag_element.name = category
                    
                    # Gestire gli attributi specifici per ogni tag
                    for attr, new_attr in attribute_map.items():
                        if attr in tag_element.attrs:
                            # Rinomina l'attributo, se presente
                            tag_element[new_attr] = tag_element[attr]
                            del tag_element[attr]  # Rimuovere l'attributo originale

        # Restituisci l'HTML modificato
        return str(soup)
    
    def convert2(self,html):
            soup = BeautifulSoup(html, 'html.parser')
            tab = {
                'Layout':{'tags':['div'],'attr':{}},
                'Text':{'tags':['p'],'attr':{}},
                'Action':{'tags':['a','form'],'attr':{'href':'route'}},
                'Graph':{'tags':['img'],'attr':{}},
            }

            for elm in tab:
                obj = tab[elm]
                for tag in obj['tags']:
                    for p_tag in soup.find_all(tag):
                        p_tag.name = elm
                        for att in p_tag.attrs.copy():
                            if att in obj['attr']:
                                p_tag[obj['attr'][att]] = p_tag[att]
                        #attributes = p_tag.attrs
            '''# Sostituire i tag HTML con i tag XML personalizzati
            for div in soup.find_all('div', class_='toast'):
                group = soup.new_tag('Group')
                window = soup.new_tag('Window')
                group.append(window)
                window.append(div.find('Row', class_='toast-body').find('p'))
                div.insert_before(group)
                div.decompose()

            for form in soup.find_all('form'):
                action = soup.new_tag('Action', actionType="submit", url=form['action'])
                for input_tag in form.find_all('input'):
                    input_tag.name = 'Input'
                    action.append(input_tag)
                for a_tag in form.find_all('a'):
                    a_tag.name = 'Action'
                    action.append(a_tag)
                form.insert_before(action)
                form.decompose()'''
            
            
            return soup.prettify()
            

    
    async def mount_view(self,root,data=dict()):
        tags = ['Messenger','Storekeeper']
        inner = []
        tag = root._name
        att = root._attributes
        text = root.cdata
        elements = root.get_elements()
        if len(elements) > 0:
            for element in elements:
                mounted = await self.mount_view(element,data)
                inner.append(mounted)
                    
        match tag:
            case 'Messenger':
                html = ''
                for item in inner:
                    html += item
                return html
            case 'Storekeeper':
                html = ''
                for item in inner:
                    html += item
                return html
            case 'Graph':
                if 'type' in att:
                    tipo = att['type']
                elif 'src' in att:
                    tipo = 'img'
                elif 'icon' in att:
                    tipo = 'icon'
                else:
                    tipo = 'None'
                
                
                match tipo:
                    case 'icon':
                        icon = att['icon'] if 'icon' in att else 'bi-image-alt'
                        out = self.code('i',{'class':f'bi {icon}'})
                        self.att(out,att)
                        return out
                    case 'img':
                        src = att['src'] if 'src' in att else 'bi-image-alt'
                        img = self.code('img',{'src':src})
                        self.att(img,att)
                        return img
                    case 'carousel':
                        ind = []
                        for item in inner:
                            self.att(item,{'class':'carousel-item'})
                            #s = self.code('button',{'data-bs-target':'test','data-bs-slide-to':'0'},[])
                            ind.append(self.code('button',{'type':'button','data-bs-target':f'#{att["id"]}','data-bs-slide-to':str(len(ind))})) 
                        self.att(ind[0],{'class':'active','aria-current':'true'})
                        self.att(inner[0],{'class':'active'})
                        carousel = self.code('div',{'class':'carousel carousel-dark slide','data-bs-ride':'carousel'},[
                            self.code('div',{'class':'carousel-indicators'},ind),
                            self.code('div',{'class':'carousel-inner'},inner)
                        ])
                        self.att(carousel,att)
                        return carousel
                    case _:
                        icon = att['icon'] if 'icon' in att else 'bi-image-alt'
                        out = self.code('i',{'class':f'bi {icon}'})
                        self.att(out,att)
                        return out
            case 'View':
                copy = data.copy()
                view = await self.builder(**copy|att)
                return self.code('div',{'class':'container-fluid d-flex flex-row col p-0 m-0'},[view])
            case 'Message':
                model = att['type'] if 'type' in att else 'flesh'
                title = att['title'] if 'title' in att else ''

                if model == 'system':
                    return self.code('div',
                        {'class':'toast','role':'alert','aria-live':'assertive','aria-atomic':'true'},[
                            self.code('div',{'class':'toast-header'}, self.code('strong',{'class':'me-auto'},title)),
                            self.code('div',{'class':'toast-body'},inner)
                        ])
                elif model == 'flesh':
                    return self.code('div',{'class':'alert alert-primary','role':'alert'},inner)
            case 'Input':
                tipo = att['type'] if 'type' in att else 'None'
                tipi = ["button","checkbox","color","date","datetime-local","email","file","hidden","image","month","number","password","radio","range","reset","search","submit","tel","text","time","url","week"]

                if tipo in tipi:
                    #form-range
                    input = self.code('input',{'class':'form-control','type':tipo})
                    self.att(input,att)
                    return input
                else:
                    input = self.code('input',{'class':'form-control','type':'text'})
                    self.att(input,att)
                    return input
            case 'Action':
                model = att['type'] if 'type' in att else 'button'
                url = att['url'] if 'url' in att else '#'
                
                if model == 'form':
                    act = att['act'] if 'act' in att else '#'
                    form = self.code('form',{'action':act,'method':'POST'},inner)
                    self.att(form,att)
                    return form
                elif model == 'button':
                    button = self.code('a',{'class':'btn rounded-0'},inner)
                    self.att(button,att)
                    return button
            case 'Window':
                tipo = att['type'] if 'type' in att else 'None'
                id = att['id'] if 'id' in att else 'None'
                action = att['action'] if 'action' in att else 'action'
                match tipo:
                    case 'canvas':
                        return self.code('div',{'data-bs-backdrop':'false','id':id,'class':'offcanvas offcanvas-end'},[
                            self.code('div',{'class':'offcanvas-body p-0 m-0'},inner),
                        ])
                    case 'modal':
                        return self.code('div',{'id':id,'class':'modal','data-bs-backdrop':'false'},[
                            self.code('div',{'class':'modal-dialog modal-dialog-centered modal-dialog-scrollable'},[
                                self.code('div',{'class':'modal-content'},[
                                    self.code('div',{'class':'modal-header'}),
                                    self.code('div',{'class':'modal-body'},inner),
                                    self.code('div',{'class':'modal-footer'},f'<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button> <button type="button" onclick="document.getElementById(\'form-{action}\').submit();" class="btn btn-success">{action.capitalize()}</button>')
                                ]),
                            ]),
                        ])
                    case _:
                        return self.code('div',{'class':'container-fluid d-flex h-100 p-0 m-0'},inner)
            case 'Text':
                tipo = att['type'] if 'type' in att else 'None'
                match tipo:
                    case 'editable':
                        text = self.code('div',{'contenteditable':'true'},text)
                        self.att(text,att)
                        return text
                    case _:
                        text = self.code('p',{'class':'text-truncate fw-lighter p-0 m-0'},text)
                        self.att(text,att)
                        return text
            case 'Group':
                tipo = att['type'] if 'type' in att else 'None'
                match tipo:
                    case 'tab':
                        #self.att(inner[0],{'class':'active show'})
                        for item in inner:
                            self.att(item,{'class':'tab-pane fade','role':'tabpanel'})
                        tab = self.code('div',{'class':'tab-content'},inner)
                        self.att(tab,att)
                        return tab
                    case 'nav':
                        new = []
                        for item in inner:
                            li = self.code('li',{'class':'nav-item'},[item])
                            new.append(li)
                        ul = self.code('ul',{'class':'nav col'},new)
                        tab = self.code('div',{'class':'d-flex align-items-center justify-content-center'},[ul])
                        self.att(ul,att)
                        self.att(tab,att)
                        return tab
                    case 'tree':
                        tab = self.code('ul',{'class':'tree p-0'},[
                            self.code('li',{'class':''},inner),
                        ])
                        self.att(tab,att)
                        return tab
                    case 'input':
                        new = []
                        for item in inner:
                            li = self.code('span',{'class':'input-group-text'},[item])
                            new.append(li)
                        tab = self.code('div',{'class':'input-group'},new)
                        self.att(tab,att)
                        return tab
                    case 'node':
                        new = [] 
                        for item in inner:
                            li = self.code('li',{'class':''},[item])
                            new.append(li)

                        tab = self.code('details',{'class':''},[
                            self.code('summary',{'class':''},text),
                            self.code('ul',{'class':''},new)
                        ])
                        
                        self.att(tab,att)
                        return tab
                    case 'accordion':
                        new = [] 
                        for item in inner:
                            li = self.code('div',{'class':'accordion-item'},[item])
                            new.append(li)

                        tab = self.code('div',{'class':'accordion'},new)
                        self.att(tab,att)
                        return tab
                    case _:
                        return self.code('div',{'class':'container-fluid p-0 m-0'},inner)
            case 'Layout':
                tt = self.code('div',{},inner)
                self.att(tt,att)
                return tt
            case _:
                id = att['id'] if 'id' in att else 'None'
                if id not in self.components:
                    self.components[id] = {'id': id}

                # Funzione per convertire ricorsivamente gli elementi in XML
                def untangle_to_xml(untangle_element):
                    attributes = ' '.join(f'{key}="{value}"' for key, value in untangle_element._attributes.items())
                    attributes = f' {attributes}' if attributes else ''

                    children_xml = ''.join(untangle_to_xml(child) for child in untangle_element.children)
                    cdata = untangle_element.cdata or ''

                    if children_xml or cdata:
                        return f'<{untangle_element._name}{attributes}>{cdata}{children_xml}</{untangle_element._name}>'
                    else:
                        return f'<{untangle_element._name}{attributes} />'

                # Convertiamo l'intera struttura in una stringa XML
                xml_str = ''.join(untangle_to_xml(child) for child in root.children)
                
                url = f'application/view/component/{tag}.xml'
                html = ''.join(x.outerHTML for x in inner)

                # Creiamo la vista
                view = await self.builder(
                    component=self.components[id],
                    attributes=att,
                    url=url,
                    inner=markupsafe.Markup(xml_str)
                )

                #view = await self.mount_view(root,data)

                self.att(view, att)
                return view
                
                  
    def mount_route(self,routes,url):
        
        gg = untangle.parse(url)
        zz = gg.get_elements()[0]
        for setting in  zz.get_elements():
            
            path = setting.get_attribute('path')
            method = setting.get_attribute('method')
            typee = setting.get_attribute('type')
            view = setting.get_attribute('view')

            if typee == 'model':
                endpoint = self.model

            if typee == 'view':
                endpoint = self.view

            if typee == 'action':
                endpoint = self.action

            if typee == 'logout':
                endpoint = self.logout

            if typee == 'login':
                endpoint = self.login

            self.views[path] = view
            r = Route(path,endpoint=endpoint, methods=[method])
            if setting == 'Mount':
                r = Mount('/static', app=StaticFiles(directory='/public'), name="static")
            routes.append(r)