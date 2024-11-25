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
          self.cash = dict()         

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

        async def on_drag_start(self,event,**constants):
          #print('on_drag_start')
          for x in self.document.querySelectorAll(".drop-target"):
            x.className += " highlight"
          self.drag = event.target.id

        async def on_drop(self,event,**constants):
          event.preventDefault()
          draggable_element = js.document.getElementById(self.drag)
          if self.drag in self.components:
            name = self.components[self.drag]
            component = js.document.getElementById(name)
            component.className = component.className.replace(' opacity-25','')
            #component.className = component.className.replace('highlight','')
            self.components[name] = name
          
          if 'maker' in self.drag and self.drag in self.components:
            self.components.pop(self.drag)

          for x in self.document.querySelectorAll(".drop-target"):
            x.className = x.className.replace('highlight','')
        
        async def on_drag_leave(self,event,**constants):
          pass
          #event.target.className = event.target.className.replace('highlight','')
        
        async def on_drag_over(self,event,**constants):
          event.preventDefault()
          draggable_element = js.document.getElementById(self.drag)
          #print(draggable_element.getAttribute('draggable-domain'),event.target.getAttribute('draggable-domain'))
          if draggable_element and draggable_element.getAttribute('draggable-domain') == event.target.getAttribute('draggable-domain'):
            
            component = draggable_element.getAttribute('draggable-component')
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
                view.className += ' highlight'
                event.target.appendChild(view)
                
            else:
              if identifier in self.components and self.components[identifier] != '':
                component = js.document.getElementById(self.components[identifier])
                if 'opacity-25' not in event.target.className:
                  component.className += ' opacity-25'
                if event.target != component and component.parentNode != event.target:
                  mouseY = event.clientY # Posizione verticale del mouse rispetto al viewport
                  containerRect = event.target.getBoundingClientRect() # Ottieni la posizione e dimensione dell'elemento di destinazione
                  containerTop = containerRect.top # La posizione in alto dell'elemento di destinazione
                  containerHeight = containerRect.height # Altezza dell'elemento di destinazione

                  # Calcola la posizione relativa del mouse all'interno dell'elemento di destinazione
                  mousePos = mouseY - containerTop

                  # Se il mouse è nella parte superiore dell'elemento, inserisci sopra, altrimenti sotto
                  if (mousePos < containerHeight / 2):
                    event.target.insertBefore(component, event.target.firstChild)
                  else:
                    event.target.appendChild(component)         
        
        async def event(self,event,**constants):
          action = event.target.getAttribute('click')
          currentElement = event.target
          attributeValue = None

          while not attributeValue: 
            attributeValue = currentElement.getAttribute('click')
            currentElement = currentElement.parentElement

          _ = await self.act(value=attributeValue)
          '''# Divisione della stringa in base al separatore '|'
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
            _ = await act(args=result[name])'''
        
        async def act(self,**constants):
          # Divisione della stringa in base al separatore '|'
          functions = constants['value'].split('|')
          # Creazione del dizionario
          lista = []

          # Iterazione su ogni funzione per estrarre chiave e parametri
          for func in functions:
            result = {}
            # Estrai il nome della funzione (prima della parentesi)
            key = re.match(r"(\w+)\(", func).group(1)
              
            # Estrai tutti i parametri in formato chiave:valore (es. 'key': 'value')
            params = re.findall(r"(\w+):'(.*?)'", func)
              
            # Converte la lista di tuple (chiave, valore) in un dizionario
            param_dict = {k: v for k, v in params}
              
            # Aggiungi la funzione e i suoi parametri come dizionario
            result[key] = param_dict
            lista.append(result)
          
          for n in lista:
            for name in n:
              module = await language.get_module(f'application/action/{name}.py',language)
              act = getattr(module,name)
              _ = await act(**n[name])
        
        def att(self,element,attributes):
          # 'property'
          base = ['id','opacity','color','shadow','border','class','width','height','visibility','position','padding','margin','expand','style','matter'],
          tt = {
            'div':[],
            'p':[],
            'matter':['color','size','alignment','position'],
            'text':['color','size','alignment','position'],
            'style':['border','opacity','class'],
            'border':['color','thickness','radius','opacity','position','style'],
          }

          sizes = ['0','1','2','3','4','5']
          events = ['click']
          colors = ['primary','primary-subtle','secondary','secondary-subtle','success','success-subtle','danger','danger-subtle','warning','warning-subtle','info','info-subtle','light','light-subtle','dark','dark-subtle','black','white']
          
          for key in attributes:
            value = attributes[key]
            match key:
              # Property
              case 'layer':pass
              case 'identifier':
                element.setAttribute('name',value)
              case 'id':
                element.setAttribute(key,value)
              case 'width':
                style = element.getAttribute('style') if type(element.getAttribute('style')) == type('') else ''
                style += f" width:{value};"
                element.setAttribute('style',style)
              case 'height':
                style = element.getAttribute('style') if type(element.getAttribute('style')) == type('') else ''
                style += f" height:{value};"
                element.setAttribute('style',style)
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
              case 'alignment-horizontal':
                enums = ['start','end','center','between','around','evenly']
                if value in enums:
                  element.className += f" justify-content-{value}"
              case 'alignment-vertical':
                enums = ['start','end','center','baseline','stretch']
                if value in enums:
                  element.className += f" align-items-{value}"
              case 'alignment-content':
                #enums = ['start','end','center','baseline','stretch']
                match value:
                  case 'vertical':
                    element.className += " d-flex flex-column"
                  case 'horizontal':
                    element.className += " d-flex flex-row"
              case 'expand':
                match value:
                  case 'vertical':
                    element.className += " h-100"
                  case 'horizontal':
                    element.className += " w-100"
                  case 'full':
                    element.className += " w-100 h-100"
                  case 'auto':
                    element.className += " col-auto"
                  case 'dynamic':
                    element.className += " col"
                  case _:
                    element.className += f" col-{value} "
              case 'collapse':
                match value:
                  case 'full':
                    element.className += " d-none"
                  case 'visibility':
                    element.className += " invisible"
              case 'flow':
                match value:
                  case 'auto':element.className += f" overflow-{value} "
                  case 'hidden':element.className += f" overflow-{value} "
                  case 'visible':element.className += f" overflow-{value} "
                  case 'scroll':element.className += f" overflow-{value} "
              # Style
              case 'text-size':
                if 'px' in value:
                  style = element.getAttribute('style') if type(element.getAttribute('style')) == type('') else ''
                  style += f' font-size: {value};'
                  element.setAttribute('style',style)
                elif value in sizes:
                  element.className += f" fs-{value}"
              case 'text-font':pass
              case 'text-color':
                if value in colors:
                  element.className += f" fs-{value}"
              case 'text-style':pass
              case 'style':
                style = element.getAttribute('style') if type(element.getAttribute('style')) == type('') else ''
                style += ' '+value
                element.setAttribute('style',style)
              case 'background':
                if '#' in value:
                    style = element.getAttribute('style') if type(element.getAttribute('style')) == type('') else ''
                    style += f" background:{value};"
                    element.setAttribute('style',style)
                else:
                  element.className += f" bg-{value}"
              case 'background-opacity':pass
              case 'background-color':pass
              case 'shadow':
                match value:
                  case'none': element.className += " shadow-none"
                  case 'lg':  element.className += " shadow-lg"
                  case'md': element.className += " shadow"
                  case'sm': element.className += " shadow-sm"
              case 'class':
                element.className += f' {value}'
              case 'border':
                element.className += f" border-{value}"
              case 'border-position':
                match value:
                  case 'outer': element.className += " border"
                  case 'top': element.className += " border-top"
                  case 'bottom': element.className += " border-bottom"
                  case 'right': element.className += " border-start"
                  case 'left': element.className += " border-end"
              case 'border-thickness':
                if value in sizes:
                  element.className += f" border-{value}"
              case 'border-radius-size':
                if value in sizes:
                  element.className += f" rounded-{value}"
              case 'border-color':
                if value in colors:
                  element.className += f" border-{value}"
              case 'border-radius':
                match value:
                  case 'pill': element.className += " rounded-pill"
                  case 'circle': element.className += " rounded-circle"
                  case 'top': element.className += " rounded-top"
                  case 'bottom': element.className += " rounded-bottom"
                  case 'right': element.className += " rounded-start"
                  case 'left': element.className += " rounded-end"
              # Event
              case 'link':
                element.setAttribute('href',value)
                element.setAttribute('data-bs-toggle','tab')
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
                element.addEventListener('dragleave',pyodide.create_proxy(self.on_drag_leave))
              case 'draggable':
                element.setAttribute(key,'true')
                element.setAttribute('ondragstart','drag(event)')
                element.setAttribute('draggable-domain',value)
                element.addEventListener('dragstart',pyodide.create_proxy(self.on_drag_start))
              case 'draggable-component':
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
          if url not in self.cash:
            response = js.fetch(url,{'method':'GET'})
            file = await response
            aa = await file.text()
            self.cash[url] = aa
            return aa
          else:
            return self.cash[url]