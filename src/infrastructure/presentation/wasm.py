import sys  

if sys.platform != 'emscripten':
  import infrastructure.presentation.starlette as starlette
  import framework.service.flow as flow
  import os


  class adapter(starlette.adapter):
      
      def info(self,**constants):
          pass

      '''@flow.async_function(ports=('storekeeper',))
      async def builder(self,storekeeper,**constants):
          print(constants)
          cwd = os.getcwd()
          f = open(f"{cwd}/public/index.html", "r")
          stringa = f.read()
          template = self.env.from_string(stringa)
          rresult = template.render({'title':'Colosso','url':'asdasdasdasdasd'})
          return rresult'''
else:
    import js
    from jinja2 import Environment, select_autoescape,FileSystemLoader,BaseLoader,ChoiceLoader,Template
    import untangle
    import asyncio
    import pyodide
    import importlib
    flow = language.load_module(area="framework",service='service',adapter='flow')

    class MyLoader(BaseLoader):
      def get_source(self, environment, template):
          req = js.XMLHttpRequest.new()
          req.open("GET", f"application/view/layout/{template}", False)
          req.send()
          return req.response, None, None
          # return TEMPLATE, fname, False
    
    class adapter():
        def __init__(self,**constants):
          self.components = dict()
          self.config = constants['config']
          http_loader = MyLoader()
          self.env = Environment(loader=http_loader,autoescape=select_autoescape(["html", "xml"]))
          self.document = js.document

        def loader(self, *services, **constants):
          code = asyncio.create_task(self.async_loader(),name="loader")
          #js.document.body.prepend(mount_view(code))
          pass

        '''async def view(self,request):
          a = await self.builder()
          print("qui")
          return HTMLResponse(a)'''
        
        def get_var(self,accessor_string,input_dict):
          """Gets data from a dictionary using a dotted accessor-string"""
          current_data = input_dict
          for chunk in accessor_string.split('.'):
              if type([]) == type(current_data):
                current_data = current_data[int(chunk)]
              else:
                current_data = current_data.get(chunk, {})
          return current_data

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

          if transaction['state']:
            user = transaction['result']
          else:
            user = dict()

          html = await self.builder(user=user)
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

        async def event(self,event,**constants):
            action = event.target.getAttribute('click')
            data = []
            if '(' in action:
              ss = action.split('(')
              action = ss[0]
              data = ss[1].replace(')','').split(',')

            
            module = await language.get_module(action)
            act = getattr(module,action)
            _ = await act(self,event,data=data)
            
            
            #print(dir(event.target),event.target.checked,self.components[target])

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
              case 'url':
                #'http://0.0.0.0:8000/'
                element.setAttribute('url',value)
                element.addEventListener('click',pyodide.create_proxy(self.route))
              case 'click':
                element.setAttribute(key,value)
                element.addEventListener('click',pyodide.create_proxy(self.event))
              case 'href':
                element.setAttribute('href',value)
              case 'icon':
                element.className += ' '+value
              case 'width':
                style = element.getAttribute('style') if type(element.getAttribute('style')) == type('') else ''
                style += f" width:{value};"
                element.setAttribute('style',style)
              case 'height':
                style = element.getAttribute('style') if type(element.getAttribute('style')) == type('') else ''
                style += f" height:{value};"
                element.setAttribute('style',style)
              case 'src':
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
                else: element.className += f" col-{value} "
                  
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

        def code(self,tag,attr,inner=None):
          tag = js.document.createElement(tag)
          for key in attr:
            tag.setAttribute(key,attr[key])
          for x in inner:
            tag.append(x)
          return tag
        
        async def mount_vieww(self,root,data=dict()):
            
          inner = []
          tag = root._name
          att = root._attributes
          text = root.cdata
          elements = root.get_elements()
          if len(elements) > 0:
            for x in elements:
              #print(root,type(data),data)
              ffff = await self.mount_view(x,data)
              inn.append(ffff)
                    
          match tag:
                case 'Button':
                  item = self.code('button',{'class':'btn'},inn)
                  self.att(item,att)
                  return item
                case 'Route':
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
                case 'Tab':
                  div = js.document.createElement("div")
                  div.className = "tab-content"
                  classe = 'nav-link'
                  self.att(div,root._attributes)
                  #print(root,data)
                  fiest = True
                  for x in inn:
                      tab = js.document.createElement("div")
                      tab.className = "tab-pane fade"
                      if fiest:
                        tab.className += " active show"
                        fiest = False

                      tab.setAttribute('role','tabpanel')
                      tab.setAttribute('id',x.getAttribute('id'))
                      x.removeAttribute('id')
                      tab.prepend(x)
                      div.prepend(tab)
                    
                  
                  return div
                case 'Row':
                  item = self.code('div',{'class':'row'},inn)
                  self.att(item,att)
                  return item
                case 'Column':
                  #div = js.document.createElement("div")
                  cell = js.document.createElement("div")
                  #div.className = "col p-0 "
                  cell.className = "d-flex flex-row"
                  #classe = 'col'
                  #self.att(div,root._attributes)
                  self.att(cell,root._attributes)
                  #div.append(cell)
                  for x in inn:
                     #col += f'<div class="col">{x}</div>'
                     cell.append(x)
                  return cell
                case 'Text':
                  div = js.document.createElement("p")
                  div.className = "fw-lighter p-0 m-1"
                  for x in inn:
                    div.append(x)
                  div.innerHTML += root.cdata
                  if 'var' in root._attributes:
                    gg = self.get_var(root._attributes['var'],data)
                    div.innerHTML += str(gg)
                  
                  #print(root.cdata)
                  self.att(div,root._attributes)
                  return div
                case 'Nav':
                  nav = js.document.createElement("nav")
                  nav.className = "container-fluid"
                  classe = "navbar"

                  self.att(nav,root._attributes)
                  ul = js.document.createElement("ul")
                  ul.className = "nav container-fluid"
                  for x in inn:
                     li = js.document.createElement("li")
                     li.className = "nav-item"
                     li.append(x)
                     ul.append(li)
                     
                  nav.append(ul)
                  return nav
                case 'Breadcrumb':
                  nav = js.document.createElement("nav")
                  nav.className = ""
                  

                  self.att(nav,root._attributes)
                  ul = js.document.createElement("ol")
                  ul.className = "breadcrumb p-0 m-0"
                  for x in inn:
                     li = js.document.createElement("li")
                     li.className = "breadcrumb-item"
                     li.append(x)
                     ul.append(li)
                     
                  nav.append(ul)
                  return nav
                case 'Container':
                  if 'type' in root._attributes:
                    div = js.document.createElement(root._attributes['type'])
                  else:
                    div = js.document.createElement("div")
                  classe = "container"
                  
                  if 'size' not in root._attributes:
                    div.className = classe
                  
                  self.att(div,root._attributes)

                  for x in inn:
                     div.append(x)
                  return div
                case 'Input':
                  
                  lType = {'':'form-control','range':'form-range','checkbox':'form-check-input','password':'form-control'}
                  
                  if 'type' in root._attributes:
                    key = root._attributes['type']
                    kk = key if key in lType else ''
                    classe = lType[kk]
                    if key not in lType:
                      div = js.document.createElement(key)
                      div.setAttribute('contenteditable','true')
                      div.innerHTML += root.cdata
                    else:
                      div = js.document.createElement('input')
                    
                    
                  else:
                    classe = lType['']
                    div = js.document.createElement("input")
                    div.setAttribute('value',root.cdata)
                  
                  div.className = classe
                  
                  
                  
                  self.att(div,root._attributes)
                  for x in inn:
                    div.append(x)

                  if 'var' in root._attributes:
                    gg = self.get_var(root._attributes['var'],data)
                    #print(gg,data)
                    #div.innerHTML += str(gg)
                    div.setAttribute('value',gg)

                  return div
                case 'Select':
                  div = js.document.createElement("select")
                  div.className = "form-select"
                  self.att(div,root._attributes)
                  for x in inn:
                    option = js.document.createElement("option")
                    option.append(x)
                    div.append(option)
                  return div
                case 'Icon':
                  div = js.document.createElement("i")
                  div.className = "bi p-1"
                  self.att(div,root._attributes)
                  return div
                case 'Alert':
                  div = js.document.createElement("div")
                  classe = 'alert'
                  alertType = root._attributes['type'] if 'type' in root._attributes else ''
                  div.setAttribute('role','alert')
                  div.className = classe + ' alert-dismissible d-flex align-items-center'
                  self.att(div,root._attributes)
                  if 'info' == alertType:
                    div.innerHTML += '<i class="bi bi-info-circle-fill px-3"></i>'
                  elif 'success' == alertType:
                    div.innerHTML += '<i class="bi bi-check-circle-fill px-3"></i>'
                  elif 'danger' == alertType:
                    div.innerHTML += '<i class="bi bi-exclamation-triangle-fill px-3"></i>'
                  elif 'warning' == alertType:
                    div.innerHTML += '<i class="bi bi-exclamation-octagon-fill px-3"></i>'
                  div.innerHTML += root.cdata
                  div.innerHTML += '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>'
                  return div
                case 'Badge':
                  div = js.document.createElement("span")
                  classe = 'badge'
                  div.className = classe
                  self.att(div,root._attributes)
                  div.innerHTML += root.cdata
                  return div
                case 'Window':
                  title = root._attributes['title'] if 'title' in root._attributes else ''
                  typee = root._attributes['type'] if 'type' in root._attributes else ''
                  idd = root._attributes['id'] if 'id' in root._attributes else ''
                  action = root._attributes['action'] if 'action' in root._attributes else ''
                  
                  div = js.document.createElement("div")
                  if typee == 'canvas':

                    header = js.document.createElement("div")
                    header.className = 'offcanvas-header'
                    header.innerHTML += f'<h5 class="offcanvas-title" id="offcanvasScrollingLabel">{title}</h5>'
                    header.innerHTML += '<button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>'
                    body = js.document.createElement("div")
                    body.className = 'offcanvas-body p-0'

                    #div.append(header)
                    div.append(body)
                    div.setAttribute('data-bs-backdrop','false')
                    classe = 'offcanvas offcanvas-end'
                  elif typee == 'main':
                    div.className = "d-flex h-100"
                    for x in inn:
                     div.append(x)
                    return div
                  else:
                    dialog = js.document.createElement("div")
                    dialog.className = 'modal-dialog modal-dialog-scrollable'
                    content = js.document.createElement("div")
                    content.className = 'modal-content'

                    header = js.document.createElement("div")
                    header.className = 'modal-header'
                    header.innerHTML += f'<h5 class="modal-title">{title}</h5>'
                    #header.innerHTML += '<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>'
                    body = js.document.createElement("div")
                    body.className = 'modal-body p-0'
                    footer = js.document.createElement("div")
                    footer.className = 'modal-footer'
                    footer.innerHTML = f'<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button> <button type="button" onclick="document.getElementById(\'form-{action}\').submit();" class="btn btn-success">{action.capitalize()}</button>'


                    classe = 'modal'

                    div.append(dialog)
                    dialog.append(content)
                    content.append(header)
                    content.append(body)
                    content.append(footer)
                    self.att(dialog,root._attributes)

                  div.className = classe
                  div.setAttribute('data-bs-backdrop','false')
                  self.att(div,root._attributes)
                  
                  

                  for x in inn:
                     body.append(x)
                  return div
                case 'Carousel':
                  classe = 'modal'
                  div = js.document.createElement("div")
                  div.className = classe
                  inner = js.document.createElement("div")
                  inner.className = 'carousel-inner'

                  for x in inn:
                     body.append(x)

                  return div
                case 'Img':
                  classe = 'img'
                  div = js.document.createElement("img")
                  div.className = classe
                  
                  self.att(div,root._attributes)

                  return div
                case 'Collapse':
                  classe = 'img'
                  div = js.document.createElement("div")
                  div.className = "collapse"
                  self.att(div,root._attributes)
                  
                  for x in inn:
                     div.append(x)

                  return div
                case 'Form':         
                  div = js.document.createElement("form")
                  self.att(div,root._attributes)
                  
                  for x in inn:
                     div.append(x)

                  return div
                case 'View':         
                  div = js.document.createElement("form")
                  #self.att(div,root._attributes)
                  url = root._attributes['url'] if 'url' in root._attributes else ''
                  cc = data.copy()
                  cc['url'] = url
                  test = await self.builder(**cc)

                  return test
                case 'Divider':         
                  div = js.document.createElement("div")
                  div.className = "vr"
                  self.att(div,root._attributes)
                  return div
                case 'Table':
                  tt = root._attributes['head'].split(';') if 'head' in root._attributes else []
                  
                  #table.className += "table"
                  table = js.document.createElement("table")
                  head = js.document.createElement("thead")
                  hrow = js.document.createElement("tr")
                  
                  for y in root.get_elements()[:1]:
                      brow = js.document.createElement("tr")
                      for z in y.children:
                        bcol = js.document.createElement("th")
                        ttt = await mount_view(z,data)
                        bcol.append(ttt)
                        brow.append(bcol)
                      head.append(brow)
                  
                  body = js.document.createElement("tbody")

                  # non è ottimizzato qui
                  for y in root.get_elements()[1:]:
                      brow = js.document.createElement("tr")
                      for z in y.children:
                        bcol = js.document.createElement("td")
                        ttt = await mount_view(z,data)
                        bcol.append(ttt)
                        brow.append(bcol)
                      body.append(brow)

                  head.append(hrow)
                  table.append(head)
                  table.append(body)
                  table.className += "table table-striped"
                  self.att(table,root._attributes)

                  return table
                case 'Mark':         
                  div = js.document.createElement("span")
                  self.att(div,root._attributes)
                  for x in inn:
                    div.append(x)
                  div.innerHTML += root.cdata
                  return div
                case 'Storekeeper':
                  model = root._attributes['model'] if 'model' in root._attributes else 'client'
                  url = f"gather?model={model}"
                  #if 'identifier' in root._attributes:
                  #  url += f"&identifier={root._attributes['identifier']}"
                  
                  if 'token' in root._attributes:
                    url += f"&token={self.cookies['session_token']}"
                  
                  
                  div = js.document.createElement("span")
                  self.att(div,root._attributes)
                  
                  response = js.fetch(url,{'method':'GET'})
                  file = await response
                  aa = await file.text()
                  bb = json.loads(aa)
                  #cccc = {'storekeeper':bb['result']}|data
                  #print(cccc)

                  for y in root.get_elements():
                    built = await mount_view(y,{'storekeeper':bb['result']}|data)
                    div.append(built)

                  return div
                case _:
                  id = root._attributes['id'] if 'id' in root._attributes else 'ttttt'
                  model = root._attributes['model'] if 'model' in root._attributes else 'client'
                  args = root._attributes['args'] if 'args' in root._attributes else None

                  if id not in self.components:
                    self.components[id] = dict({'id':id,'model':model,'selected':[],'pageCurrent':1,'pageRow':10,'sortField':'CardName','sortAsc':True})
                  
                  #response = js.fetch(f"gather?model={self.components[id]['model']}&row={self.components[id]['pageRow']}&page={self.components[id]['pageCurrent']}&order={self.components[id]['sortField']}",{'method':'GET'})
                  #file = await response
                  #aa = await file.text()
                  #bb = json.loads(aa)
                  #self.components[id]['data'] = bb 
                  url = f'application/view/component/{tag.replace("C_","")}.xml'
                  
                  
                  test = await self.builder(url=url,component=self.components[id],args=args)
                  
                  return test
                
        
        #@flow.async_function(ports=('storekeeper',))
        async def builder(self,**constants):
          
          if 'url' not in constants:
            url="application/view/layout/app.xml"
          else:
            url = constants['url']
          
          if 'view' not in constants: 
            response = js.fetch(url,{'method':'GET'})
            file = await response
            aa = await file.text()
          else:
            aa = constants['view']

          template = self.env.from_string(aa)
          transformed = template.render(constants)
          obj = untangle.parse(transformed)
          
          
          return await self.mount_view(obj.children[0],constants)
          