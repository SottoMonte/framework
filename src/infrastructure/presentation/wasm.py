import sys  
if sys.platform != 'emscripten':
  import infrastructure.presentation.starlette as starlette
  import framework.service.flow as flow
  import os
  from starlette.responses import JSONResponse,HTMLResponse,RedirectResponse
else:
  import js
  from jinja2 import Environment, select_autoescape,FileSystemLoader,BaseLoader,ChoiceLoader,Template
  import untangle
  import asyncio
  import pyodide
  import importlib
  import uuid
  import re
    
  flow = language.load_module(area="framework",service='service',adapter='flow')
  starlette = language.load_module(area="infrastructure",service='presentation',adapter='starlette')

  class MyLoader(BaseLoader):
      def get_source(self, environment, template):
          req = js.XMLHttpRequest.new()
          req.open("GET", f"application/view/layout/{template}", False)
          req.send()
          return req.response, None, None


class adapter(starlette.adapter):
  if sys.platform != 'emscripten':
    async def view(self,request):
        #html = await self.builder(file=self.views[request.url.path])
        text = await self.host({'url':'application/view/layout/wasm.html'})
        template = self.env.from_string(text)
        html = template.render()
        return HTMLResponse(html)
  else:
        def __init__(self,**constants):
          self.components = dict()
          self.config = constants['config']
          http_loader = MyLoader()
          self.env = Environment(loader=http_loader,autoescape=select_autoescape(["html", "xml"]))
          self.document = js.document         

        def loader(self, *services, **constants):
          code = asyncio.create_task(self.async_loader(),name="loader")
          #js.document.body.prepend(mount_view(code))

        @flow.async_function(ports=('storekeeper',))
        async def async_loader(self, storekeeper, **constants):
          #session = js.window.sessionStorage.getItem('session_state')
          #socket = js.WebSocket.new('ws://localhost:8000/ws')
          #def on_message(event):
          #  print(f"Message received: {event.data}")
          #socket.onmessage = on_message
          #pyodide.create_proxy(self.route)
          #socket.addEventListener('message', pyodide.create_proxy(on_message))
          #cookies = {cookie.split('=')[0].strip():cookie.split('=')[1] for cookie in js.document.cookie.split(';')}
          self.cookies = {}
          for cookie in js.document.cookie.split(';'):
              if '=' in cookie:
                  key, value = cookie.split('=', 1)
                  self.cookies[key.strip()] = value
          #print(js.document.cookie,"<-----",session,cookies)

          model = 'user'
          token = self.cookies['session_token'] if 'session_token' in self.cookies else 'None'
          
          transaction = await storekeeper.get(model="user",token=token)

          print(transaction)

          if transaction['state']:
            user = transaction['result']
          else:
            user = dict()
          try:
            html = await self.builder(user=user)
          except Exception as e:
            print("errore generico",e)
          print(html)
          js.document.getElementById('loading').remove()
          js.document.body.prepend(html)
        
        def info(self):
          return ('front-end')

        async def route(self,event,**constants):
          currentElement = event.target
          attributeValue = None

          while not attributeValue: 
            attributeValue = currentElement.getAttribute('url')
            currentElement = currentElement.parentElement

          code = await self.builder(url=attributeValue)
          js.document.getElementById('main').innerHTML = ''
          js.document.getElementById('main').prepend(code)
          '''
            # currentTarget
            url = handle.target.getAttribute('url')
            href = handle.target.getAttribute('href')
            #print(url)
            code = await self.builder(url=url,href=href)
            js.document.getElementById('main').innerHTML = ''
            js.document.getElementById('main').prepend(code)'''

        async def on_drag_start(self,event,**constants):
          
          self.drag = event.target.id

        async def on_drop(self,event,**constants):
          draggable_element = js.document.getElementById(self.drag)
          if self.drag in self.components:
            name = self.components[self.drag]
            component = js.document.getElementById(name)
            component.className = component.className.replace(' opacity-25','')
            self.components[name] = name
          
          if 'maker' in self.drag and self.drag in self.components:
            self.components.pop(self.drag)
        
        async def on_drag_over(self,event,**constants):
          event.preventDefault()
          draggable_element = js.document.getElementById(self.drag)
          if draggable_element and draggable_element.getAttribute('draggable-domain') == event.target.getAttribute('draggable-domain'):
            
            component = draggable_element.getAttribute('draggable-type')
            identifier = self.drag
            
            if component and identifier not in self.components:
                self.components[identifier] = ""
                #self.components[identifier] = identifier
                  #self.components[identifier] = dict({'id':identifier,'selected':[],'pageCurrent':1,'pageRow':10,'sortField':'CardName','sortAsc':True})
                url = f'application/view/component/{component}.xml'
                #view = await self.builder(url=url,component=self.components[identifier])
                attr = dict()
                for i in list(draggable_element.attributes):
                  attr[i.name] = i.value
                view = await self.builder(url=url,**attr)
                view.className += ' opacity-25'
                self.components[identifier] = view.getAttribute('id')
                  #self.components[identifier]['id'] = view.getAttribute('id')
                
                event.target.appendChild(view)
            else:
              if self.components[identifier] != '':
                component = js.document.getElementById(self.components[identifier])
                component.className += ' opacity-25'
                event.target.appendChild(component)
        
        async def event(self,event,**constants):
          action = event.target.getAttribute('click')
          currentElement = event.target
          attributeValue = None

          while not attributeValue: 
            attributeValue = currentElement.getAttribute('click')
            currentElement = currentElement.parentElement

          # Divisione della stringa in base al separatore '|'
          functions = attributeValue.split('|')

          # Creazione del dizionario
          result = {}

          # Iterazione su ogni funzione per estrarre chiave e parametri
          for func in functions:
              key = re.match(r"(\w+)\(", func).group(1)
              params = re.findall(r"'(.*?)'", func)
              result[key] = params
          
          for name in result:
            module = await language.get_module(f'application/action/{name}.py',language)
            act = getattr(module,name)
            _ = await act(args=result[name])
        
        async def act(self,**constants):
          # Divisione della stringa in base al separatore '|'
          functions = constants['value'].split('|')

          # Creazione del dizionario
          result = {}

          # Iterazione su ogni funzione per estrarre chiave e parametri
          for func in functions:
              # Estrai il nome della funzione (prima della parentesi)
              key = re.match(r"(\w+)\(", func).group(1)
              
              # Estrai tutti i parametri in formato chiave:valore (es. 'key': 'value')
              params = re.findall(r"(\w+):'(.*?)'", func)
              
              # Converte la lista di tuple (chiave, valore) in un dizionario
              param_dict = {k: v for k, v in params}
              
              # Aggiungi la funzione e i suoi parametri come dizionario
              result[key] = param_dict
          
          for name in result:
            module = await language.get_module(f'application/action/{name}.py',language)
            act = getattr(module,name)
            _ = await act(**result[name])

        def att(self,element,attributes):
          for key in attributes:
            value = attributes[key]
            match key:
              case 'alignment':
                element.className += f" align-items-{value} "
              case 'content':
                element.className += f" justify-content-{value} "
              case 'action':
                element.setAttribute(key,value)
              case 'method':
                element.setAttribute('method',value)
              case 'identifier':
                element.setAttribute('name',value)
              case 'route':
                element.setAttribute('url',value)
                element.addEventListener('click',pyodide.create_proxy(self.route))
              case 'click':
                element.setAttribute(key,value)
                element.addEventListener('click',pyodide.create_proxy(self.event))
              case 'init':
                element.setAttribute(key,value)
                asyncio.create_task(self.act(value=value))
              case 'droppable':
                element.setAttribute('ondragover','allowDrop(event)')
                element.setAttribute('draggable-domain',value)
                element.addEventListener('drop',pyodide.create_proxy(self.on_drop))
                element.addEventListener('dragover',pyodide.create_proxy(self.on_drag_over))
              case 'draggable':
                element.setAttribute(key,'true')
                element.setAttribute('ondragstart','drag(event)')
                element.setAttribute('draggable-domain',value)
                element.addEventListener('dragstart',pyodide.create_proxy(self.on_drag_start))
              case 'link':
                element.setAttribute('href',value)
              case 'icon':
                element.className += ' '+value
              case 'width':
                style = element.getAttribute('style') if type(element.getAttribute('style')) == type('') else ''
                style += f" width:{value};"
                element.className += ' col-auto'
                element.setAttribute('style',style)
              case 'height':
                style = element.getAttribute('style') if type(element.getAttribute('style')) == type('') else ''
                style += f" height:{value};"
                element.className += ' col-auto'
                element.setAttribute('style',style)
              case 'src':
                element.setAttribute(key,value)
              case 'role':
                element.setAttribute(key,value)
              case 'id':
                element.setAttribute(key,value)
              case 'disabled':
                element.setAttribute('disabled','')
              case 'readonly':
                element.setAttribute('readonly','')
              case 'type':
                #element.setAttribute('type',value)
                if element.tagName in ['INPUT','BUTTON']:element.setAttribute(key,value)
                elif 'alert' in element.className: element.className += f" alert-{value} "
                else:element.className += f" {value} "
              case 'target':
                element.setAttribute('data-bs-toggle','modal')
                element.setAttribute('data-bs-target',value)
              case 'data-bs-target':
                element.setAttribute('data-bs-target',value)
              case 'data-toggle':
                element.setAttribute(key,value)
              case 'data-bs-toggle':
                element.setAttribute('data-bs-toggle',value)
              case 'data-bs-dismiss':
                element.setAttribute(key,value)
              case 'position':
                if 'modal-dialog' in element.className:
                  element.className += f" modal-dialog-{value} "
                else:
                  style = element.getAttribute('style') if type(element.getAttribute('style')) == type('') else ''
                  style += f"position:{value};"
                  element.setAttribute('style',style)
              case 'top':
                style = element.getAttribute('style') if type(element.getAttribute('style')) == type('') else ''
                style += f"top:{value};"
                element.setAttribute('style',style)
              case 'start':
                style = element.getAttribute('style') if type(element.getAttribute('style')) == type('') else ''
                style += f"start:{value};"
                element.setAttribute('style',style)
              case 'end':
                style = element.getAttribute('style') if type(element.getAttribute('style')) == type('') else ''
                style += f"end:{value};"
                element.setAttribute('style',style)
              case 'size':
                if value == 'full': element.className += " w-100 h-100"
                elif value == 'elastic': element.className += " flex-grow-1"
                elif value == 'expand': element.className += " d-flex h-100 flex-column"
                elif value == 'fluid': element.className += " container-fluid p-0 m-0"
                elif 'modal-dialog' in element.className: element.className += f" modal-{value} "
                elif element.tagName == 'BUTTON': element.className += f" btn-{value} "
                elif value == 'auto': element.className += " col-auto"
                elif value == 'expanded': element.className += " col"
                else: element.className += " col"
                  
              case 'color':
                if element.tagName in ['DIV','NAV','FOOTER']:
                  msg = f" background:{value};"
                elif element.tagName in ['P']:
                  msg = f" text-{value}"
                else :
                  msg = ''
                
                if '#' in value or 'rgba' in value:
                  a = element.getAttribute('style') if type(element.getAttribute('style')) == type('') else ''
                  a += msg
                  element.setAttribute('style',a)
                else:
                  element.className += msg

              case 'style':
                style = element.getAttribute('style') if type(element.getAttribute('style')) == type('') else ''
                style += ' '+value
                element.setAttribute('style',style)
              case 'class':
                element.className += ' '+value
              case 'margin':
                if ';' in value:
                  pp = value.split(';')
                  for x in pp:
                    element.className += ' '+x
                else:
                  element.className += ' '+value
              case 'padding':
                if ';' in value:
                  pp = value.split(';')
                  for x in pp:
                    element.className += ' '+x
                else:
                  element.className += ' '+value
              case 'target':
                element.setAttribute('data-bs-toggle','modal')
                element.setAttribute('data-bs-target',value)
              case 'selected':
                element.setAttribute(value,'')
              case _:
                element.setAttribute(key,value)
        
        async def rebuild(self,id,tag,**constants):
                  
          #response = js.fetch(f"gather?model={self.components[id]['model']}&row={self.components[id]['pageRow']}&page={self.components[id]['pageCurrent']}&order={self.components[id]['sortField']}",{'method':'GET'})
          #file = await response
          #aa = await file.text()
          #bb = json.loads(aa)

          url = f'application/view/component/{tag.replace("C_","")}.xml'
                  
                  
          test = await self.builder(url=url,component=self.components[id])

          cc = self.document.getElementById(id)
          cc.innerHTML = ""
          for x in test.childNodes:
            #print(dir(test))
            cc.append(x)
          #cc.replaceChild(test,cc)
          #return test

        def code(self,tag,attr,inner=[]):
          tag = js.document.createElement(tag)
          for key in attr:
            tag.setAttribute(key,attr[key])

          if type(inner) == type([]):
            for item in inner:
              tag.append(item)
          elif type(inner) == type(''):
            tag.innerHTML += inner
          else:
            pass
          return tag
        
        async def host(self,constants):
          if 'url' not in constants:
            url="application/view/layout/app.xml"
          else:
            url = constants['url']
          response = js.fetch(url,{'method':'GET'})
          file = await response
          aa = await file.text()
          return aa