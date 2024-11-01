

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
except Exception as e:
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
        out = await self.mount_view(xml.children[0],constants)
        return out
        
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
                icon = att['icon'] if 'icon' in att else 'bi-image-alt'
                if 'icon' in att:
                    return self.code('i',{'class':f'bi {icon}'})
                elif 'src' in att:
                    src = att['src'] if 'src' in att else 'bi-image-alt'
                    img = self.code('img',{'src':src})
                    self.att(img,att)
                    return img
                else:
                    return self.code('i',{'class':f'bi {icon}'})
            case 'View':
                copy = data.copy()
                test = await self.builder(**copy|att)
                return self.code('div',{'class':'container-fluid d-flex flex-row col p-0 m-0'},[test])
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
                return self.code('input',{'class':'form-control'})
            case 'Action':
                model = att['type'] if 'type' in att else 'button'
                url = att['url'] if 'url' in att else '#'
                
                if model == 'form':
                    act = att['act'] if 'act' in att else '#'
                    form = self.code('form',{'action':act,'method':'POST'},inner)
                    self.att(form,att)
                    return form
                elif model == 'button':
                    button = self.code('a',{'class':'btn','href':url},inner)
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
            case 'Panel':
                html = ''
                for item in inner:
                    html += item
                return html
            case 'Text':
                return self.code('p',{'class':'fw-lighter'},text)
            case 'Group':
                return self.code('div',{'class':'container-fluid p-0 m-0'},inner)
            case 'Row':
                tt = self.code('div',{'class':'d-flex flex-column row p-0 m-0'},inner)
                self.att(tt,att)
                return tt
            case 'Column':
                tt = self.code('div',{'class':'d-flex flex-row col p-0 m-0'},inner)
                self.att(tt,att)
                return tt
            case 'Container':
                tt = self.code('div',{'class':'container-fluid p-0 m-0'},inner)
                self.att(tt,att)
                return tt
            case _:
                pass
                  
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