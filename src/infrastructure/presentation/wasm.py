import sys

modules = {'flow': 'framework.service.flow','starlette': 'infrastructure.presentation.starlette'}

if sys.platform != 'emscripten':
  import os
  from starlette.responses import JSONResponse,HTMLResponse,RedirectResponse
else:
  import js
  from jinja2 import Environment, select_autoescape,FileSystemLoader,BaseLoader,ChoiceLoader,Template,DebugUndefined,Undefined
  import untangle
  import asyncio
  import pyodide
  import importlib
  import uuid
  import re
  import json
  import ast

  class MyLoader(BaseLoader):
      def get_source(self, environment, template):
          req = js.XMLHttpRequest.new()
          req.open("GET", f"application/view/layout/{template}", False)
          req.send()
          return req.response, None, None


class adapter(starlette.adapter):
  if sys.platform != 'emscripten':
    async def view(self,request):
        #html_page = await self.builder(url=self.views[request.url.path])
        #print('BOOM',self.views[request.url.path],html_page)
        #print('tututut',request.session)
        file = await self.host({'url':'application/view/layout/wasm.html'})
        template = self.env.from_string(file)
        html_template = template.render()
        #html_template = html_template.replace('<!-- Body -->',html_page)
        return HTMLResponse(html_template)
  else:
        def __init__(self, **constants):
          print("🚀 Inizializzazione del modulo WASM...")

          # Inizializza le variabili di istanza
          self.components = {}
          self.config = constants.get('config', {})  # Evita KeyError con .get()
          self.cash = {}
          self.cookies = {}
          self.data = {}
          self.views = {}
          # Configura il loader per i template
          http_loader = MyLoader()
          self.env = Environment(loader=http_loader, undefined=DebugUndefined, autoescape=select_autoescape(["html", "xml"]))
          self.env.filters['get'] = language.get_safe
          
          # Riferimento al documento JavaScript
          self.document = js.document

          print("✅ Modulo WASM inizializzato correttamente.")

        @flow.synchronous(managers=('storekeeper',))
        def loader(self, storekeeper, **constants):
          z = asyncio.create_task(self.bond(),name="bond")
          code = asyncio.create_task(self.async_loader(),name="loader")
          
        
        @flow.asynchronous(managers=("messenger", "storekeeper", "defender"))
        async def async_loader(self, messenger,storekeeper,defender, **constants):
              
              url = self.config['routes'].replace('src/','')
              data = await self.host({'url':url})
              self.mount_route(None,data)
              await messenger.post(domain="debug",message="🔄 Avvio async_loader...")
              # Estrai i cookie in modo più sicuro
              self.cookies = {
                  key.strip(): value
                  for cookie in js.document.cookie.split(';') if '=' in cookie
                  for key, value in [cookie.split('=', 1)]
              }
              
              await messenger.post(domain="debug",message=f"📜 Cookies: {self.cookies}")
              
              # Recupera il token di sessione in modo più sicuro
              session = self.cookies.get('session', 'None')
              session = eval(session)
              identifier = self.cookies.get('session_identifier', 'None')
              #session = eval(session)
              print(session,identifier,type(session),type(identifier),'TIKTIK')
              
              await defender.unionsession(session=session,identifier=identifier)
              #await messenger.post(domain="debug",message=f"🔑 Token recuperato: {session}")

              # Recupera i dati dell'utente con il token
              #transaction = await storekeeper.gather(model="user", token=token)
              transaction = await defender.whoami2(token=session)
              await messenger.post(domain="debug",message=f"📦 Transazione ricevuta: {transaction}")

              # Verifica se la transazione è riuscita
              transaction = {'state':False} if transaction == None else transaction
              user = transaction.get('result', {})[0] if transaction.get('state') else {}
              
              

              # Costruisce l'HTML con i dati dell'utente
              html_template = await self.builder(user=user,session=session)
              html_page = await self.builder(url=self.views[js.window.location.pathname],user=user,session=session)

              # Rimuove l'elemento di caricamento
              loading_element = self.document.getElementById('loading')
              if loading_element:
                  loading_element.remove()
                  await messenger.post(domain="debug",message="✅ Elemento di caricamento rimosso.")

              # Aggiunge il contenuto alla pagina
              self.document.body.prepend(html_template)
              main = self.document.getElementById('main')
              main.appendChild(html_page)

              if transaction.get('state'):
                await messenger.post(domain="debug",message=f"👤 Dati utente: {user}")
                await messenger.post(domain="success",message="✅ Utente autenticato con successo.")
              else:
                await messenger.post(domain="error",message=transaction.get('error','Errore sconosciuto'))

              await messenger.post(domain="debug",message="✅ Contenuto aggiornato con i dati utente.")
              

        @flow.asynchronous(managers=('messenger',))
        async def bond(self,messenger,**constants):
          print("🔗 Avvio bond...")
          while True:
            print("🔄 Esecuzione del ciclo di polling...")
            msg = await messenger.read(domain="*")
            print(msg,'BONDmsg')
            domains = msg.get('domain',[])
            print(constants,'BOND',domains,msg)
            '''ok = []
            for x in self.data.keys():
                
                matching_domains = language.wildcard_match([domain], x)
                if len(matching_domains) == 1:
                    ok.append(x)
            print(ok,self.data)'''
            for domain in domains:
              for id  in self.data.get(domain,[]):
                self.components[id].setdefault('messenger',[]).append(msg)
                await self.rebuild(id,self.components[id].get('view'),message=msg)

            for id  in self.data.get('*',[]):
              self.components[id].setdefault('messenger',[]).append(msg)
              await self.rebuild(id,self.components[id].get('view'),message=msg)
              


        async def open_dropdown(self,event,**constants):
          
          if event.button == 2:  # Click sinistro del mouse
            # Ottieni l'elemento dropdown
            currentElement = event.target
            dropdown_button = None

            while not dropdown_button and currentElement:
              cerca = currentElement.querySelector('.dropdown-menu')
              if cerca:
                dropdown_button = currentElement
              currentElement = currentElement.parentElement

            if dropdown_button:
              # Ottieni le coordinate del click del mouse
              # Mostra il dropdown
              dropdown = js.bootstrap.Dropdown.getOrCreateInstance(dropdown_button)
              dropdown.toggle()       
            else:
                print("Elemento dropdown non trovato")
          

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
          print('on_drop',event.target.id)
          draggable_element = js.document.getElementById(self.drag)
          
          if self.drag in self.components:
            target = js.document.getElementById(event.target.id)
            #print(self.components[self.drag])
            data_drag = target.getAttribute('droppable-data')
            #print('data_drag',data_drag)
            name = self.components[self.drag].get('id')
            component = js.document.getElementById(name)
            component.className = component.className.replace(' opacity-25','')
            
            #component.className = component.className.replace('highlight','')
            await self.act(value=draggable_element.getAttribute('draggable-event').replace(')',",data:'"+str(data_drag)+"')"))
          
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
                self.components[identifier] = {'id':view.getAttribute('id')}
                  #self.components[identifier]['id'] = view.getAttribute('id')
                view.className += ' highlight'
                event.target.appendChild(view)
                #print("BOOOOOM")
                
            else:
              if identifier in self.components and self.components[identifier] != '':
                #component = js.document.getElementById(self.components[identifier])
                component = js.document.getElementById(self.components[identifier]['id'])
                #print(component)
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
            
              
            
            # Aggiungi la funzione e i suoi parametri come dizionario
            result[key] = language.extract_params(func)
            lista.append(result)
          
          for n in lista:
            for name in n:
              #module = await language.get_module(f'application/action/{name}.py',language)
              module = await language.load_module(language,path=f'application.action.{name}',area='application',service='action',adapter=name)
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
              case 'space':
                element.className += f" gap-{value}"
              case 'id':
                element.setAttribute(key,value)
              case 'width':
                style = element.getAttribute('style') if type(element.getAttribute('style')) == type('') else ''
                style += f" max-width:{value};width:{value};"
                element.setAttribute('style',style)
              case 'height':
                style = element.getAttribute('style') if type(element.getAttribute('style')) == type('') else ''
                style += f" max-height:{value};height:{value};"
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
              case 'type':
                element.setAttribute(key,value)
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
              case 'hide':
                mode,target = value.split(':')
                mode = mode.strip().lower()
                target = target.strip()
                element.setAttribute('data-bs-dismiss',mode)
              case 'show':
                mode,target = value.split(':')
                mode = mode.strip().lower()
                target = target.strip()
                match mode:
                  case 'modal':
                    element.setAttribute('data-bs-target','#'+target)
                    element.setAttribute('data-bs-toggle',mode)
                  case 'offcanvas':
                    element.setAttribute('data-bs-target','#'+target)
                    element.setAttribute('data-bs-toggle',mode)
                  
              case 'ddd':
                element.addEventListener('contextmenu',pyodide.ffi.create_proxy(self.open_dropdown))
              case 'link':
                element.setAttribute('href',value)
              case 'route':
                if ':' in value:
                  mode,target = value.split(':',1)
                  mode = mode.strip().lower()
                  target = target.strip()
                  match mode:
                    case 'link':
                      element.setAttribute('href',target)
                    case _:
                      element.setAttribute('data-bs-toggle',mode)
                      element.setAttribute('href','#'+target)
                else:
                  element.setAttribute('url',value)
                  element.addEventListener('click',pyodide.ffi.create_proxy(self.route))
              case 'click':
                element.setAttribute(key,value)
                element.addEventListener('click',pyodide.ffi.create_proxy(self.event))
              case 'onchange':
                element.setAttribute(key,value)
                element.addEventListener('onchange',pyodide.ffi.create_proxy(self.event))
              case 'init':
                element.setAttribute(key,value)
                asyncio.create_task(self.act(value=value))
              case 'droppable':
                element.setAttribute('ondragover','allowDrop(event)')
                element.setAttribute('draggable-domain',value)
                element.addEventListener('drop',pyodide.ffi.create_proxy(self.on_drop))
                element.addEventListener('dragover',pyodide.ffi.create_proxy(self.on_drag_over))
                element.addEventListener('dragleave',pyodide.ffi.create_proxy(self.on_drag_leave))
              case 'draggable':
                element.setAttribute(key,'true')
                element.setAttribute('ondragstart','drag(event)')
                element.setAttribute('draggable-domain',value)
                element.addEventListener('dragstart',pyodide.ffi.create_proxy(self.on_drag_start))
              case 'draggable-component':
                element.setAttribute(key,value)
              case 'draggable-event':
                element.setAttribute(key,value)
              case 'droppable-data':
                element.setAttribute(key,value)
              
        async def rebuild(self, id, tag, **data):
          try:
              await asyncio.sleep(1)

              #url = f"application/view/component/{tag}.xml"
              url = tag
              new_component = await self.builder(url=url, component=self.components[id], **data)

              old_component = self.document.getElementById(id)

              if old_component is None:
                  raise ValueError(f"Elemento con id '{id}' non trovato nel documento.")

              parent = old_component.parentNode
              if parent is None:
                  raise ValueError(f"L'elemento con id '{id}' non ha un nodo genitore.")

              # Sostituzione corretta
              #for x in new_component.childNodes:
              #  old_component.append(x)
              parent.replaceChild(new_component, old_component)

          except Exception as e:
              print(f"Errore durante la ricostruzione del componente '{id}': {e}")
        
        async def rebuild3(self,id,tag,**data):
                  
          #response = js.fetch(f"gather?model={self.components[id]['model']}&row={self.components[id]['pageRow']}&page={self.components[id]['pageCurrent']}&order={self.components[id]['sortField']}",{'method':'GET'})
          #file = await response
          #aa = await file.text()
          #bb = json.loads(aa)
          await asyncio.sleep(1)
          #url = f"application/view/component/{tag}.xml"
          url = tag
                  
                  
          test = await self.builder(url=url,component=self.components[id],**data)

          cc = self.document.getElementById(id)
          cc.replaceChild(test,cc)
          #cc.innerHTML = ""
          #for x in test.childNodes:
            #print(dir(test))
          #  cc.append(x)
          #cc.replaceChild(test,cc)
          #return test

        def mount_route(self, routes, url):
          route_map = {
              'model': self.model,
              'view': self.view,
              'action': self.action,
              'logout': self.logout,
              'login': self.login
          }

          for setting in untangle.parse(url).get_elements()[0].get_elements():
              path = setting.get_attribute('path')
              method = setting.get_attribute('method')
              typee = setting.get_attribute('type')
              view = setting.get_attribute('view')

              self.views[path] = view
              #route = Mount('/static', app=StaticFiles(directory='/public'), name='static') \
              #    if setting == 'Mount' else Route(path, endpoint=route_map.get(typee), methods=[method])

              #routes.append(route)

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