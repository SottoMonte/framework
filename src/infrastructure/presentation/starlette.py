import framework.port.presentation as presentation
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

'''class AuthenticationMiddleware:
    def __init__(
        self,
        app ,
        backend,
        login_manager = None,
        excluded_dirs = [],
        allow_websocket: bool = True,
    ):
        self.app = app
        self.backend = backend
        self.excluded_dirs = excluded_dirs or []
        self.login_manager = login_manager
        #self.secret_key = login_manager.secret_key
        self.allow_websocket = allow_websocket

    async def __call__(
        self, scope: Scope, receive: Receive, send: Send
    ) -> None:
        if self.allow_websocket is False and scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        elif scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return

        conn = HTTPConnection(scope=scope, receive=receive)
        #print(dir(conn))
        #print(conn.session.items())
        print(conn.cookies)
        #print(conn.scope)
        #print('/logout' == conn['path'],conn['path'])
        if '/logout' == conn['path']:
            self.login_manager.logout()
            conn.cookies = dict()
            print('LOGOUT')
        
        print(self.login_manager)
        
        if not user or user.is_authenticated is False:
            conn.scope["user"] = self.login_manager.anonymous_user_cls()
        else:
            conn.scope["user"] = user

        async def custom_send(message: Message):
            #print(message)
            user_ = conn.scope["user"] if 'user' in conn.scope else None
            name = user_['username'] if user_ != None and 'username' in user_ else ''
            passs = user_['password'] if user_ != None and 'password' in user_ else ''
            
            ccc = await self.login_manager.authenticate(username=name,password=passs)

            if ccc:
                #print(user_)
                message.setdefault("headers", [])
                headers = MutableHeaders(scope=message)
                cookie: "http.cookies.BaseCookie[str]" = http.cookies.SimpleCookie()
                key = 'user'
                if 'password' in user_:
                    del user_['password']
                cookie[key] = user_
                
                if 'expires' not in cookie[key]:
                    cookie[key]["expires"] = 36000
                if 'path' not in cookie[key]:
                    cookie[key]["path"] = '/'
                if 'domain' not in cookie[key]:
                    cookie[key]["domain"] = '/'
                if 'secure' not in cookie[key]:
                    cookie[key]["secure"] = True

                headers["set-cookie"] = cookie.output(header="").strip()

                #print(headers)
                #message[headers]
            await send(message)

        await self.app(scope, receive, custom_send)
        return'''
    
class AuthorizationMiddleware:
    def __init__(
        self,
        app ,
        manager,
        allow_websocket: bool = True,
    ):
        self.app = app
        self.manager = manager
        self.allow_websocket = allow_websocket

    async def __call__(
        self, scope: Scope, receive: Receive, send: Send
    ) -> None:
        if self.allow_websocket is False and scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        elif scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return

        for prefix_dir in ['/github','/static','/login','/logout','/framework','/application','/infrastructure']:
            if scope["path"].startswith(prefix_dir) or scope["path"] == '/':
                await self.app(scope, receive, send)
                return

        conn = HTTPConnection(scope=scope, receive=receive)
        ssss = conn.cookies['session_identifier'] if 'session_identifier' in conn.cookies else None
        #print(ssss,conn.cookies)

        check = await self.manager.authenticated(session=ssss)

        if not check:
            response = RedirectResponse('/', status_code=301)
            await response(scope, receive, send)
            return
        else:
            await self.app(scope, receive, send)
            return

class adapter(presentation.presentation):

    @flow.function(ports=('defender',))
    def __init__(self,defender,**constants):
        self.config = constants['config']
        print(self.config)
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
            Middleware(AuthorizationMiddleware, manager=defender)
            #Middleware(CORSMiddleware, allow_origins=['*'],allow_methods=['*'],allow_headers=['*']),
            #Middleware(DefenderMiddleware,backend=self,manager=defender),
            #Middleware(DefenderMiddleware,backend=self,manager=defender,allow_websocket=False,),
        ]

        self.app = Starlette(debug=True,routes=routes,middleware=middleware)

    def loader(self, *services, **constants):
        fs_loader = FileSystemLoader("src/application/view/layout/")
        #http_loader = MyLoader()
        #choice_loader = ChoiceLoader([fs_loader, http_loader])
        self.env = Environment(loader=fs_loader,autoescape=select_autoescape(["html", "xml"]))
        loop=constants['loop']
        config = Config(app=self.app, loop=loop,host=self.config['host'], port=int(self.config['port']),use_colors=True,reload=True)
        server = Server(config)
        loop.create_task(server.serve())

    async def builder(self,**constants):
        f = open(constants['file'], "r")
        html = f.read()

        template = self.env.from_string(html)
          
        content = template.render(constants)

        #obj = untangle.parse(transformed)
        
        #return await mount_view(obj.children[0],constants)
        return content
        
    @flow.async_function(ports=('defender',))
    async def logout(self,request,defender) -> None:
        assert request.scope.get("app") is not None, "Invalid Starlette app"
        request.session.clear()
        response = RedirectResponse('/', status_code=303)
        response.delete_cookie("session_token")
        return response

    @flow.async_function(ports=('storekeeper','defender',))
    async def login(self,request: Request, storekeeper, defender) -> None:
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
        html = await self.builder(file=self.views[request.url.path] )
        return HTMLResponse(html)
    
    async def mount_view(root,data=dict()): 
        inner = []
        tag = root._name
        elements = root.get_elements()
        if len(elements) > 0:
            for element in elements:
                mounted = await mount_view(element,data)
                inner.append(mounted)
                    
        match tag:
            case 'Messenger':
                pass
            case 'Storekeeper':
                pass
            case 'Graph':
                pass
            case 'View':
                pass
            case 'Notice':
                pass
            case 'Input':
                div = js.document.createElement("a")
                div.className = "nav-link p-1 d-flex flex-row"
                classe = 'nav-link'
                self.att(div,root._attributes)
                for x in inn:
                    if 'url' in root._attributes:
                        x.setAttribute('url',root._attributes['url'])
                    if 'href' in root._attributes:
                        x.setAttribute('href',root._attributes['href'])
                    div.append(x)
                return div
            case 'Action':
                # url,
                pass
            case 'Window':
                pass
            case 'Panel':
                pass
            case 'Text':
                pass
            case 'Row':
                pass
            case 'Column':
                pass
            case 'Container':
                pass
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