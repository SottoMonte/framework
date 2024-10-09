import framework.port.presentation as presentation
import framework.service.flow as flow
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse,HTMLResponse,RedirectResponse
from starlette.routing import Route
from starlette.routing import Mount
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from jinja2 import Environment, PackageLoader, select_autoescape

import untangle

import os
import uuid
#import uvicorn
from uvicorn import Config, Server

# Auth 
#from starlette.middleware.sessions import SessionMiddleware
from datetime import timedelta
#from starlette_login.middleware import AuthenticationMiddleware

#
from starlette.requests import HTTPConnection
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from starlette.datastructures import MutableHeaders
import http.cookies

class AuthenticationMiddleware:
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
        
        '''if not user or user.is_authenticated is False:
            conn.scope["user"] = self.login_manager.anonymous_user_cls()
        else:
            conn.scope["user"] = user'''

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
        return
    
class AuthorizationMiddleware:
    def __init__(
        self,
        app ,
        allow_websocket: bool = True,
    ):
        self.app = app
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
        ssss = conn.cookies['user'] if 'user' in conn.cookies else None
        #print(ssss)
        SessionAuthBackend
        if False:
            response = RedirectResponse('/', status_code=301)
            await response(scope, receive, send)
            return
        else:

            await self.app(scope, receive, send)
            return

class DefenderMiddleware:
    def __init__(
        self,
        app ,
        backend = None,
        manager = None,
        excluded_dirs = [],
        allow_websocket: bool = True,
    ):
        self.app = app
        self.backend = backend
        self.excluded_dirs = excluded_dirs or []
        self.manager = manager
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
        session = conn.session.get('user')
        print(conn.cookies,session)
        
        

        async def custom_send(message: Message):
            #print(message)
            '''user_ = conn.scope["user"] if 'user' in conn.scope else dict()
            name = user_['username'] if user_ != None and 'username' in user_ else ''
            passs = user_['password'] if user_ != None and 'password' in user_ else ''
            #print(user_)
            user = await self.manager.authenticate(username=name,password=passs)
            if user:
                self.backend.set_cookie(message,user)'''
            
            await send(message)

        await self.app(scope, receive, custom_send)
        return

class adapter(presentation.presentation):

    #@flow.function(ports=('defender',))
    def __init__(self,**constants):
        self.config = constants['config']
        cwd = os.getcwd()

        routes=[
            Mount('/static', app=StaticFiles(directory=f'{cwd}/public/'), name="static"),
            Mount('/framework', app=StaticFiles(directory=f'{cwd}/src/framework'), name="y"),
            Mount('/application', app=StaticFiles(directory=f'{cwd}/src/application'), name="z"),
            Mount('/infrastructure', app=StaticFiles(directory=f'{cwd}/src/infrastructure'), name="x"),
        ]

        self.mount_r(routes,self.config['routes'])

        middleware = [
            Middleware(CORSMiddleware, allow_origins=['*'],allow_methods=['*'],allow_headers=['*']),
            #Middleware(SessionMiddleware, secret_key='secret'),
            #Middleware(DefenderMiddleware,backend=self,manager=defender,allow_websocket=False,),
            #Middleware(AuthorizationMiddleware,)
        ]

        self.app = Starlette(debug=True,routes=routes,middleware=middleware)

    async def builder(self,**constants):
        
        return '''<html><body><form action="/create" method="post">
            <input type="text" id="model" name="model" value="client"><br>
            <label for="fname">First name:</label><br>
            <input type="text" id="name" name="identifier" value="C00011631"><br>
            <label for="lname">Last name:</label><br>
            
            <input type="text" id="lname" name="person.note" value="Rappresentante legale"><br><br>
            <input type="text" id="lname" name="name" value="Doe"><br><br>
            <input type="text" id="lname" name="person.first" value="Doe"><br><br>
            <input type="submit" value="Submit">
            </form> </body></html>'''

    async def logout(self,request) -> None:
        assert request.scope.get("app") is not None, "Invalid Starlette app"
        #login_manager = getattr(request.app.state, "login_manager", None)
        #assert login_manager is not None, LOGIN_MANAGER_ERROR

        '''config = login_manager.config
        session_key = config.SESSION_NAME_KEY
        session_fresh = config.SESSION_NAME_FRESH
        session_id = config.SESSION_NAME_ID
        remember_cookie = config.REMEMBER_COOKIE_NAME
        remember_seconds = config.REMEMBER_SECONDS_NAME

        if session_key in request.session:
            request.session.pop(session_key)

        if session_fresh in request.session:
            request.session.pop(session_fresh)

        if session_id in request.session:
            request.session.pop(session_id)

        if remember_cookie in request.session:
            request.session[remember_cookie] = "clear"
            if remember_seconds in request.session:
                request.session.pop(remember_seconds)'''

        self.clear_cookie(request.scope)

        request.session.clear()

        #request.scope["user"] = None

        return RedirectResponse('/', status_code=303)

    async def login(self,request: Request) -> None:
        request.session.update({"data": "session_data"})
        return RedirectResponse('/', status_code=303)

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
                query = request.query_params
                id = str(uuid.uuid4())
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
    
    def get_cookie(self, cookie: str):
        return decode_cookie(cookie, self.secret_key)
    
    def clear_cookie(self, message: Message) -> Message:
        headers = MutableHeaders(scope=message)
        cookie: "http.cookies.BaseCookie[str]" = http.cookies.SimpleCookie()
        #message.setdefault("headers", [])
        headers["set-cookie"] = cookie.output(header="").strip()
    
    def set_cookie(self, message, valor) -> Message:
        COOKIE_NAME = 'user'
        COOKIE_DOMAIN=None
        COOKIE_PATH='/'
        COOKIE_SECURE=False
        COOKIE_HTTPONLY=True
        COOKIE_SAMESITE=None
        COOKIE_DURATION=timedelta(days=365)

        key = COOKIE_NAME
        value = valor
        expires = int(COOKIE_DURATION.total_seconds())
        path = COOKIE_PATH
        domain = COOKIE_DOMAIN
        secure = COOKIE_SECURE
        httponly = COOKIE_HTTPONLY
        samesite = COOKIE_SAMESITE

        message.setdefault("headers", [])
        headers = MutableHeaders(scope=message)
        cookie: "http.cookies.BaseCookie[str]" = http.cookies.SimpleCookie()

        cookie[key] = value
        if expires is not None:
            cookie[key]["expires"] = expires
        if path is not None:
            cookie[key]["path"] = path
        if domain is not None:
            cookie[key]["domain"] = domain
        if secure:
            cookie[key]["secure"] = True
        if httponly:
            cookie[key]["httponly"] = True
        if samesite is not None:
            assert samesite.lower() in [
                "strict",
                "lax",
                "none",
            ], "samesite must be either 'strict', 'lax' or 'none'"
            cookie[key]["samesite"] = samesite

        headers["set-cookie"] = cookie.output(header="").strip()
        return message

    async def view(self,request):
        
        a = await self.builder()
        return HTMLResponse(a)
    
    def mount_r(self,routes,url):
        
        gg = untangle.parse(url)
        zz = gg.get_elements()[0]
        for setting in  zz.get_elements():
            
            path = setting.get_attribute('path')
            method = setting.get_attribute('method')
            typee = setting.get_attribute('type')

            if typee == 'model':
                endpoint = self.model

            if typee == 'view':
                endpoint = self.view

            if typee == 'action':
                endpoint = self.action

            if typee == 'logout':
                endpoint = self.logout

            
            r = Route(path,endpoint=endpoint, methods=[method])
            if setting == 'Mount':
                r = Mount('/static', app=StaticFiles(directory='/home/salvatore-addivinola/Documenti/accent/public/'), name="static")
            routes.append(r)
        
    def loader(self, *services, **constants):
        
        self.env = Environment()
        loop=constants['loop']
        config = Config(app=self.app, loop=loop,host=self.config['host'], port=int(self.config['port']),use_colors=True,reload=True)
        server = Server(config)
        loop.create_task(server.serve())
        
        #loop.run_until_complete(server.serve())
        #uvicorn.run(self.app, host=self.config['host'], port=int(self.config['port']),use_colors=True,loop=constants['loop'])