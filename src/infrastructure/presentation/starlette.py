import uuid

from html import escape
import json
try:
    #import framework.port.presentation as presentation
    import framework.service.flow as flow

    from starlette.applications import Starlette
    from starlette.requests import Request
    from starlette.responses import JSONResponse,HTMLResponse,RedirectResponse
    from starlette.routing import Route,Mount,WebSocketRoute
    from starlette.middleware import Middleware
    from starlette.websockets import WebSocket
    from starlette.middleware.sessions import SessionMiddleware
    from starlette.middleware.cors import CORSMiddleware
    from starlette.staticfiles import StaticFiles
    from jinja2 import Environment, select_autoescape,FileSystemLoader,BaseLoader,ChoiceLoader,Template

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
    import paramiko
    import asyncio
    import xml.etree.ElementTree as ET
    from xml.sax.saxutils import escape
    import untangle
except Exception as e:
    import untangle
    import markupsafe
    from bs4 import BeautifulSoup
    flow = language.load_module(area="framework",service='service',adapter='flow')
    starlette = None
    import xml.etree.ElementTree as ET
    from xml.sax.saxutils import escape
    print("errore generico",e)

#presentation.presentation
class adapter():

    @flow.synchronous(managers=('defender',))
    def __init__(self,defender,**constants):
        self.config = constants['config']
        self.views = dict({})
        self.ssh = {}
        cwd = os.getcwd()

        routes=[
            Mount('/static', app=StaticFiles(directory=f'{cwd}/public/'), name="static"),
            Mount('/framework', app=StaticFiles(directory=f'{cwd}/src/framework'), name="y"),
            Mount('/application', app=StaticFiles(directory=f'{cwd}/src/application'), name="z"),
            Mount('/infrastructure', app=StaticFiles(directory=f'{cwd}/src/infrastructure'), name="x"),
            WebSocketRoute("/messenger", self.websocket, name="messenger"),
            WebSocketRoute("/ssh", self.websocketssh, name="ssh"),
        ]

        self.mount_route(routes,self.config['routes'])

        middleware = [
            Middleware(SessionMiddleware, session_cookie="session_state",secret_key=self.config['project']['key']),
            Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*']), 
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
        with open('src/'+constants['url'], 'r', encoding='utf-8') as file:
            text = file.read()
            return text

    async def builder(self,**constants):
        try:
            if 'text' in constants:
                text = constants['text']
            else:
                text = await self.host(constants)
            template = self.env.from_string(text)
            content = template.render(constants)
            xml = ET.fromstring(content)
            view = await self.mount_view(xml,constants)
            return view
        except Exception as e:
            print("errore generico",e)
        
    @flow.asynchronous(managers=('defender',))
    async def logout(self,request,defender) -> None:
        assert request.scope.get("app") is not None, "Invalid Starlette app"
        request.session.clear()
        response = RedirectResponse('/', status_code=303)
        response.delete_cookie("session_token")
        return response

    @flow.asynchronous(managers=('storekeeper','defender',))
    async def login(self,request, storekeeper, defender) -> None:
        client_ip = request.client.host
        match request.method:
            case 'GET':
                query = dict(request.query_params)
                session_identifier = request.cookies.get('session_identifier', secrets.token_urlsafe(16))
                #session_token = request.cookies.get('session_token', 'Cookie not found')
                token = await defender.authenticate(ip=client_ip,identifier=session_identifier,**query)
                
                transaction = await storekeeper.gather(model="user",token=token)
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
                token = await defender.authenticate(ip=client_ip,identifier=session_identifier,**credential)
                transaction = await storekeeper.gather(model="user",token=token)
                
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
        #await websocket.close() 

    @flow.asynchronous(managers=('defender',))
    async def websocketssh(self, websocket,defender):
        ip = websocket.client.host
        accept = await defender.authorize(ip=ip)
        print(accept,ip)
        if not accept:
            print(f"Connessione rifiutata per IP non autorizzato: {ip}")
            await websocket.close()  # Chiudi con un codice di errore personalizzato

        session = await defender.whoami(ip=ip)
        
        await websocket.accept()
        
        initial_message = await websocket.receive_text()  

        print(f"Sessione {session} con messaggio iniziale: {initial_message}")
        params = json.loads(initial_message)  # Decodifica il JSON
        username = params.get("username")
        password = params.get("password")
        host = params.get("host")

        if session not in self.ssh:
            self.ssh[session] = paramiko.SSHClient()
            self.ssh[session].set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh[session].connect(host, username=username, password=password)
        channel = self.ssh[session].invoke_shell()

        # Stampa la risposta iniziale del canale
        if channel.recv_ready():
            initial_response = channel.recv(1024).decode('utf-8')
            await websocket.send_text(initial_response)

        async def read_from_channel():
            while True:
                if channel.recv_ready():
                    await websocket.send_text(channel.recv(1024).decode('utf-8'))
                await asyncio.sleep(0.01)

        async def read_from_websocket():
            while True:
                data = await websocket.receive_text()
                if data:
                    channel.send(data)

        await asyncio.gather(read_from_channel(), read_from_websocket())

        await websocket.close()

    @flow.asynchronous(managers=('storekeeper',))
    async def model(self,request,storekeeper,**constants):
        print(request.url.path)
        #form = await request.form()
        #code="C00011615",name="Marco Rullo",firstName="Marco",lastName="Rullo",gender='f'
        #print(dict(form))
        #b = await storekeeper.get(model='client',identifier=form['identifier'])
        a = await storekeeper.get(name='router',model='router',identifier='04B4FE83486D',value={'model': 'router','anno':400})
        return JSONResponse(a)
    
    @flow.asynchronous(managers=('storekeeper','messenger'))
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
            

    @flow.asynchronous(managers=('storekeeper','messenger'))
    async def mount_view(self,root,data,storekeeper,messenger):
        tags = ['Messenger','Graph','Message','Input','Action','Window','Text','Group','Layout']
        inner = []

        tag = root.tag
        att = root.attrib
        text = root.text
        elements = list(root)

        if len(elements) > 0 and tag in tags:
            for element in elements:
                mounted = await self.mount_view(element, data)
                inner.append(mounted)
                    
        match tag:
            case 'Messenger':
                model = att['type'] if 'type' in att else 'flesh'
                title = att['title'] if 'title' in att else ''
                #msg = await messenger.read()
                html = ''
                for item in inner:
                    html += item
                return html
            case 'Storekeeper':
                method = att['method'] if 'method' in att else 'overview'
                new = []
                print(att)
                match method:
                    case 'overview':
                        transaction = await storekeeper.overview(**att)
                    case 'gather':
                        transaction = await storekeeper.gather(**att)
                    case _:
                        print('Method not found')
                for y in elements:
                    built = await self.mount_view(y,{'storekeeper':transaction}|data)
                    new.append(built)
                table = self.code('div',{'class':'w-100 h-100'},new)
                self.att(table,att)
                return table
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
                        out = self.code('i',{'class':f'bi {icon}','type':'icon'})
                        self.att(out,att)
                        return out
                    case 'img':
                        src = att['src'] if 'src' in att else 'bi-image-alt'
                        img = self.code('img',{'src':src})
                        self.att(img,att)
                        return img
                    case 'table':
                        table = self.code('table',{'class':'table'},inner)
                        self.att(table,att)
                        return table
                    case 'table.head':
                        row = []
                        for x in inner:
                            th = self.code('th',{},[x])
                            row.append(th)
                        tr = self.code('tr',{},row)
                        thead = self.code('thead',{},[tr])
                        return thead
                    case 'table.body':
                        new = []
                        storekeeper = data.get('storekeeper', {})
                        mmm = storekeeper.get('result', {})
                        keys = list(mmm.keys())

                        if keys and mmm.get(keys[0], []):
                            for i in range(0, len(mmm[keys[0]])):
                                passare = {}
                                for key in keys:
                                    passare[key] = mmm[key][i]
                                built = await self.mount_view(elements[0],{'storekeeper': passare})
                                new.append(built)
                        tbody = self.code('tbody', {}, new)
                        self.att(tbody, att)
                        return tbody
                    case 'table.row':
                        row = []
                        for x in inner:
                            th = self.code('td',{},[x])
                            row.append(th)
                        tr = self.code('tr',{},row)
                        self.att(tr,att)
                        return tr
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
                view = await self.builder(**data|att)
                a = self.code('div',{'class':'container-fluid d-flex flex-row col p-0 m-0'},[view])
                return a.firstElementChild
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
                valor = att['value'] if 'value' in att else ''
                placeholder = att['placeholder'] if 'placeholder' in att else ''
                match tipo:
                    case 'select':
                        options = []
                        for x in inner:
                            if 'selected' in x.className:
                                option = self.code('option',{'selected':'selected'},[x])
                            else:
                                option = self.code('option',{},[x])
                            options.append(option)
                        input = self.code('select',{'class':'form-select'},options)
                        self.att(input,att)
                        return input
                    case 'checkbox':
                        input = self.code('input',{'class':'form-check form-check-input','type':'checkbox'})
                        self.att(input,att)
                        return input
                    case 'radio':
                        input = self.code('input',{'class':'form-check form-check-input','type':'radio'})
                        self.att(input,att)
                        return input
                    case 'switch':
                        input = self.code('input',{'class':'form-check form-switch form-check-input','type':'checkbox','role':'switch'})
                        self.att(input,att)
                        return input
                    case 'color':
                        input = self.code('input',{'class':'form-control form-control-color','type':'color'})
                        self.att(input,att)
                        return input
                    case 'range':
                        input = self.code('input',{'class':'form-range','type':'range'})
                        self.att(input,att)
                        return input
                    case _:
                        input = self.code('input',{'class':'form-control','type':'text','value':valor,'placeholder':placeholder})
                        self.att(input,att)
                        return input
            case 'Action':
                model = att['type'] if 'type' in att else 'button'
                url = att['url'] if 'url' in att else '#'
                valor = att['value'] if 'value' in att else ''
                match model:
                    case 'form':
                        action = att['action'] if 'action' in att else '#'
                        form = self.code('form',{'action':action,'method':'POST'},inner)
                        self.att(form,att)
                        return form
                    case 'button':
                        button = self.code('a',{'class':'btn rounded-0','value':valor},inner)
                        self.att(button,att)
                        return button
                    case 'dropdown':
                        new = []
                        id = att.get('id','None')
                        for item in inner[1:]:
                            li = self.code('li',{'class':'dropdown-item'},[item])
                            new.append(li)
                        ul = self.code('ul',{'class':'dropdown-menu','id':f"{id}-ul"},new)
                        btn = self.code('div',{'class':'d-inline-flex','id':f"{id}-btn"},[inner[0]])
                        button = self.code('a',{'class':'p-0 m-0','value':valor,'oncontextmenu':'return false;'},[btn,ul])
                        self.att(btn,{'ddd':'dropdown()'})
                        self.att(button,att)
                        return button
                    case _:
                        button = self.code('a',{'class':'btn rounded-0','value':valor},inner)
                        self.att(button,att)
                        return button
            case 'Window':
                tipo = att['type'] if 'type' in att else 'None'
                id = att['id'] if 'id' in att else 'None'
                action = att['action'] if 'action' in att else 'action'
                size = att['size'] if 'size' in att else 'lg'
                match tipo:
                    case 'canvas':
                        return self.code('div',{'data-bs-backdrop':'false','id':id,'class':'offcanvas offcanvas-end'},[
                            self.code('div',{'class':'offcanvas-body p-0 m-0'},inner),
                        ])
                    case 'window':
                        url = att['url'] if 'url' in att else ''
                        obj =  self.code('iframe',{'src':url,'id':id,'style':'border:none;'},[])
                        self.att(obj,att)
                        return obj
                    case 'modal':
                        btn_act = self.code('button',{'class':'btn btn-success'},[action.capitalize()])
                        self.att(btn_act,{'click':f"form(id:'form-{action}',action:'{action}')"})
                        # 'onclick':f'document.getElementById(\'form-{action}\').submit();'
                        return self.code('div',{'id':id,'class':'modal','data-bs-backdrop':'false'},[
                            self.code('div',{'class':f'modal-dialog modal-{size} modal-dialog-centered modal-dialog-scrollable'},[
                                self.code('div',{'class':'modal-content'},[
                                    self.code('div',{'class':'modal-header'}),
                                    self.code('div',{'class':'modal-body'},inner),
                                    self.code('div',{'class':'modal-footer'},[
                                        self.code('button',{'class':'btn btn-secondary','data-bs-dismiss':'modal'},['Close']),
                                        btn_act
                                    ])
                                ]),
                            ]),
                        ])
                    case _:
                        return self.code('div',{'class':'container-fluid d-flex h-100 p-0 m-0'},inner)
            case 'Text':
                tipo = att['type'] if 'type' in att else 'None'
                if 'storekeeper' in data and 'storekeeper' in att:
                    text = language.get(att['storekeeper'],data['storekeeper'])
                    #print(att['storekeeper'],'text',data['storekeeper'])
                
                match tipo:
                    case 'editable':
                        if text:
                            text = escape(text)
                        text = self.code('div',{'contenteditable':'true'},text)
                        self.att(text,att)
                        return text
                    case _:
                        if text:
                            text = escape(text)
                        obj = self.code('p',{'class':'text-truncate fw-lighter p-0 m-0','type':'data'},text)
                        self.att(obj,att)
                        return obj
            case 'Group':
                tipo = att['type'] if 'type' in att else 'None'
                match tipo:
                    case 'breadcrumb':
                        new = []
                        for item in inner:
                            li = self.code('li',{'class':'breadcrumb-item'},[item])
                            new.append(li)
                        ol = self.code('ol',{'class':'breadcrumb'},new)
                        nav = self.code('nav',{'aria-label':'breadcrumb'},[ol])
                        self.att(nav,att)
                        return nav
                    case 'tab':
                        self.att(inner[0],{'class':'active show'})
                        for item in inner:
                            self.att(item,{'class':'tab-pane fade','role':'tabpanel'})
                        tab = self.code('div',{'class':'d-flex flex-row tab-content'},inner)
                        self.att(tab,att)
                        return tab
                    case 'nav':
                        new = []
                        if len(inner) != 0:
                            self.att(inner[0],{'class':'active','aria-selected':'true'})   
                        for item in inner:
                            li = self.code('li',{'class':'nav-item'},[item])
                            new.append(li)
                        tab = self.code('ul',{'class':'nav'},new)
                        self.att(tab,att)
                        return tab
                    case 'tree':
                        tab = self.code('ul',{'class':'tree p-0'},[
                            self.code('li',{'class':'pe-4'},inner),
                        ])
                        self.att(tab,att)
                        return tab
                    case 'input':
                        new = []
                        for item in inner:
                            #print(dir(item))
                            #item_attr = item._attributes
                            #tipo = item_attr['type'] if 'type' in item_attr else None
                            tipo = item.getAttribute('type')
                            classe = item.getAttribute('class')
                            if tipo and tipo in ['data','icon','range']:  
                                expand = 'col' if ' col' in classe else ''
                                li = self.code('span',{'class':f'input-group-text rounded-0 {expand}'},[item])
                                new.append(li)
                            else:
                                self.att(item,{'class':'rounded-0'})
                                new.append(item)           
                               
                        tab = self.code('div',{'class':'input-group'},new)
                        self.att(tab,att)
                        return tab
                    case 'node':
                        new = [] 
                        for item in inner[1:]:
                            li = self.code('li',{'class':''},[item])
                            new.append(li)

                        tab = self.code('details',{'class':''},[
                            self.code('summary',{'class':''},[inner[0]]),
                            self.code('ul',{'class':''},new)
                        ])
                        
                        self.att(tab,att)
                        return tab
                    case 'accordion':
                        new = []
                        id = "#accordionExample"
                        cc = 0
                        for item in inner:
                            
                            if item.tagName not in ['A']:
                                #body = self.code('div',{'class':''},[item])
                                li = self.code('div',{'class':'accordion-collapse collapse show','data-bs-parent':id,'id':str(cc)},[item])
                                cc += 1
                            else:
                                bb = self.code('div',{'class':'accordion-button py-0','type':'button','data-bs-toggle':'collapse','data-bs-target':f'#{str(cc)}'},[item])
                                li = self.code('div',{'class':'accordion-header'},[bb])
                            #li = self.code('div',{'class':''},[hh1,cola])
                            new.append(li)

                        tab = self.code('div',{'class':'accordion','id':id},new)
                        self.att(tab,att)
                        return tab
                    case _:
                        return self.code('div',{'class':'container-fluid p-0 m-0'},inner)
            case 'Layout':
                tt = self.code('div',{},inner)
                self.att(tt,att)
                return tt
            case _:
                def elements_to_xml_string(elements):
                    # Crea un elemento root temporaneo
                    root = ET.Element('root')
                    
                    # Aggiungi tutti gli elementi alla root temporanea
                    for element in elements:
                        root.append(element)
                    
                    # Converti l'elemento root temporaneo in una stringa XML
                    xml_string = ET.tostring(root, encoding='unicode', method='xml')
                    
                    # Rimuovi il tag root temporaneo
                    xml_string = xml_string.replace('<root>', '').replace('</root>', '').replace('<root />','').strip()
                    
                    return xml_string
                if 'text' in data:
                    data.pop('text')
                xml_string = elements_to_xml_string(elements)
                url = f'application/view/component/{tag}.xml'
                #attrii = ''.join(x.outerHTML for x in att)
                id = att['id'] if 'id' in att else str(uuid.uuid1())
                if id not in self.components:
                    self.components[id] = {'id': id}
                    self.components[id]['view'] = f'application/view/component/{tag}.xml'
                    self.components[id]['inner'] = f"<{tag} id='{id}' model='repository'>{markupsafe.Markup(xml_string)}</{tag}>"
                    self.components[id]['attributes'] = att

                inner = markupsafe.Markup(xml_string)
                print(tag,'-',id)
                argg = data|{
                    'component':self.components[id],
                    'url':url,
                    'inner':inner,
                }

                
                
                # Creiamo la vista per il componente
                view = await self.builder(**argg)

                #view = await self.mount_view(root,data)

                self.att(view, att|{'type':tag})
                return view
                                 
    def mount_route(self,routes,url):
        gg = untangle.parse(url)
        print(gg)
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