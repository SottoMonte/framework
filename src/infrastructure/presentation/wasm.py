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

        async def route(self,handle,**constants):
            # currentTarget
            url = handle.target.getAttribute('url')
            href = handle.target.getAttribute('href')
            #print(url)
            code = await self.builder(url=url,href=href)
            js.document.getElementById('main').innerHTML = ''
            js.document.getElementById('main').prepend(code)

        async def on_drag_start(self,event,**constants):
          print('on_drag_start')
          self.gg = event.target.id
          
          for x in self.document.querySelectorAll(".nested"):
            x.className += " ui-droppable-active active"
        

        async def on_drop(self,event,**constants):
          print('on_drop')
          for x in self.document.querySelectorAll(".nested"):
            x.className = x.className.replace('ui-droppable-active','')
            x.className = x.className.replace('active','')
          event.preventDefault()
          if 'nested' in event.target.className:
            draggable_element = js.document.getElementById(self.gg)
            event.target.appendChild(draggable_element)
          else:
            draggable_element = js.document.getElementById(self.gg)
            a = event.target.querySelectorAll(".nested")
            if len(a) == 0 :
              #print(event.target.parentElement.tagName,event.target.parentElement.className)
              b = event.target.parentElement.querySelectorAll(".nested")
              b[0].appendChild(draggable_element)
            else:
              a[0].appendChild(draggable_element)
          #event.target.innerHTML += '<div class=" item"><p class="text-truncate fw-lighter p-0 m-0" style=" background-color:#ccc;">3</p><div class="nested ui-droppable ui-sortable"></div></div>'
        
        async def on_drag_over(self,event,**constants): 
          print('on_drag_over')
          #event.preventDefault()
        
        async def event(self,event,**constants):
            action = event.target.getAttribute('click')
            print(event)
            '''data = []
            if '(' in action:
              ss = action.split('(')
              action = ss[0]
              data = ss[1].replace(')','').split(',')

            
            module = await language.get_module(action)
            act = getattr(module,action)
            _ = await act(self,event,data=data)
            
            
            #print(dir(event.target),event.target.checked,self.components[target])'''

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
                for child in element.childNodes:
                  child.setAttribute('url',value)
                element.setAttribute('url',value)
                element.addEventListener('click',pyodide.create_proxy(self.route))
              case 'click':
                element.setAttribute(key,value)
                element.addEventListener('click',pyodide.create_proxy(self.event))
              case 'droppable':
                element.setAttribute('ondragover','allowDrop(event)')
                element.addEventListener('drop',pyodide.create_proxy(self.on_drop))
                element.addEventListener('dragover',pyodide.create_proxy(self.on_drag_over))
              case 'draggable':
                if value not in ['false','true']:
                  element.setAttribute(key,value)
                else:
                  element.setAttribute(key,'true')
                element.setAttribute('ondragstart','drag(event)')
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
                #element.setAttribute(key,value)
                pass
        
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