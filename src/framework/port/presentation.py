from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET
from jinja2 import Environment, select_autoescape,FileSystemLoader,BaseLoader,ChoiceLoader,Template,DebugUndefined
from html import escape

modules = {'flow': 'framework.service.flow'}

class port(ABC):
    tags = {
        'Resource':{},
        'Media':{'type': ['image', 'video', 'audio', 'embed']},
        'View':{},
        'Messenger':{},
        'Defender':{},
        'Graph':{},
        'Storekeeper':{},
        'Input':{'type': ['text', 'select', 'checkbox', 'textarea', 'radio', 'switch', 'color', 'range']},
        'Action':{},
        'Window':{},
        'Text':{},
        'Group':{},
        'Layout':{},
    }

    elements = [
        'Text',
        'Icon',
        'Video',
        'Row',
        'Column',
        'Container',
        'TextField',
        'Button',
        'List',
    ]


    def initialize(self):
        fs_loader = FileSystemLoader("src/application/view/layout/")
        #http_loader = MyLoader()
        #choice_loader = ChoiceLoader([fs_loader, http_loader])
        self.env = Environment(loader=fs_loader,autoescape=select_autoescape(["html", "xml"]),undefined=DebugUndefined)

    @abstractmethod
    async def mount_property(self, *services, **constants):
        pass

    @abstractmethod
    async def mount_route(self, *services, **constants):
        pass

    @abstractmethod
    async def mount_view(self, *services, **constants):
        pass

    @abstractmethod
    async def render_view(self, *services, **constants):
        pass

    @abstractmethod
    async def mount_css(self, *services, **constants):
        pass

    async def host(self,constants):
        with open('src/'+constants['url'], 'r', encoding='utf-8') as file:
            text = file.read()
            return text
    
    #@flow.asynchronous()
    async def builder(self,**constants):
        if 'application/view/component/.xml' == constants.get('url'):
            print('KANBOOOM!',constants)
        #print('BUILD41',constants)
        #try:
        if 'text' in constants:
            text = constants['text']
        else:
            text = await self.host(constants)

        template = self.env.from_string(text)
        if 'data' not in constants:
            constants['data'] = {}
        if 'view' not in constants:
            constants['view'] = {}
        
        #if self.user:
        #    constants['user'] = self.user

        content = template.render(constants)
        print('CONTENT',content)
        xml = ET.fromstring(content)
        print(xml)
        view = await self.mount_view(xml,constants)
        #await self.mount_css(view)
        return view
    
    async def rebuild(self, *services, **constants):
        pass

    @flow.asynchronous(managers=('storekeeper','messenger'))
    async def mount_view(self,root,data,storekeeper,messenger):
        inner = []

        tag = root.tag
        att = root.attrib
        text = root.text
        elements = list(root)

        if len(elements) > 0 and tag in self.tags:
            for element in elements:
                mounted = await self.mount_view(element, data)
                inner.append(mounted)
        
        #if tag in self.tags:
        #    return await self.tags[tag]()
        match tag:
            case 'Defender':
                # Implementazione di un controllo di sicurezza base per prevenire attacchi OWASP comuni
                # come XSS, SQL Injection, ecc. su codice/text stampato dal componente Defender.
                # Esegue escaping e validazione degli attributi e del testo.

                # Esempio: verifica e sanifica tutti gli attributi e il testo
                sanitized_att = {}
                for k, v in att.items():
                    # Escape HTML per evitare XSS
                    sanitized_att[k] = escape(str(v))

                # Sanifica il testo (se presente)
                sanitized_text = escape(text) if text else ''

                # Controllo su inner: se sono stringhe, esegui escape, se sono elementi, ricorsione
                sanitized_inner = []
                for item in inner:
                    if isinstance(item, str):
                        sanitized_inner.append(escape(item))
                    else:
                        sanitized_inner.append(item)  # Se è già un elemento HTML/XML, si presume sia gestito

                # Costruisci il markup sicuro per Defender
                defender_html = self.code('div', {'class': 'defender-component', **sanitized_att}, sanitized_inner or sanitized_text)
                self.att(defender_html, sanitized_att)
                return defender_html
            case 'Messenger':
                id = att['id'] if 'id' in att else str(uuid.uuid4())
                model = att['type'] if 'type' in att else 'flesh'
                title = att['title'] if 'title' in att else ''
                domain = att['domain'] if 'domain' in att else []
                view = att['view'] if 'view' in att else ''
                domain = domain.split(',')
                #self.data[domain] = {'domain':domain,'messages':messages}
                if id not in self.components:
                    for dom in domain:
                        self.data.setdefault(dom,[]).append(id)
                    
                    self.components[id] = {'id': id}
                    self.components[id]['view'] = f'application/view/component/{view}.xml'
                    #self.components[id]['inner'] = f"<{tag} id='{id}' model='repository'>{markupsafe.Markup(xml_string)}</{tag}>"
                    self.components[id]['attributes'] = att
                
                if data.get('url') != self.components[id]['view']:
                    item = await self.builder(**data|{'component':self.components[id],'url':self.components[id]['view']})
                    self.att(item,att)
                    return item
                else:
                    item = self.code('div',{'id':id,'class':'container-fluid'},inner)
                    self.att(item,att)
                    return item
            case 'Storekeeper':
                method = att['method'] if 'method' in att else 'overview'
                new = []
                payload = att['payload'] if 'payload' in att else ''
                payload = language.extract_params(payload)
                filter = att['filter'] if 'filter' in att else ''
                filter = language.extract_params(filter)
                repository = att['repository'] if 'repository' in att else 'repository'

                print(payload,repository,'transactionok')

                try:
                    match method:
                        case 'overview':
                            transaction = await storekeeper.overview(repository=repository,filter=filter,payload=payload)
                        case 'gather':
                            transaction = await storekeeper.gather(repository=repository,filter=filter,payload=payload)
                        case _:
                            print('Method not found')
                except Exception as e:
                    print('Error',e)

                print(transaction,payload,repository,'###333')
                
                for y in elements:
                    built = await self.mount_view(y,data|{'storekeeper':transaction})
                    new.append(built)
                table = self.code('div',{'class':'w-100'},new)
                self.att(table,att)
                return table
            case 'Media':
                #resource
                kind = att['type'] if 'type' in att else 'image'
                src = att['src'] if 'src' in att else None
                if src:
                    resource = await self.compose_view('VideoMedia',src)
                    inner.append(resource)

                if kind == 'video':
                    return await self.compose_view('Video',inner)
            case 'View':
                
                if 'storekeeper' in data and 'storekeeper' in att:
                    if type(data['storekeeper']) == type(dict()):
                        text = str(language.get(att['storekeeper'],data['storekeeper']))
                    else:
                        text = str(data['storekeeper'])
                    view = await self.builder(**data|{'text':text})
                elif 'code' in data and 'code' in att:
                    print('View-data:',data)
                    view = await self.builder(**data|{'text':data['code']})
                elif 'url' in att:
                    dataview = None
                    if 'data' in att:
                        dataview = att['data']
                        dataview = language.get(dataview,data['storekeeper'])
                    view = await self.builder(**data|{'url':att['url'],'data':dataview})
                    view = self.code_update(view, {}, inner,'start')
                elif 'content' in att:
                    view = await self.builder(**data|{'url':'application/view/content/'+att['content']})
                else:
                    view = None

                if 'id' in att:
                    id = att.get('id')
                    if id not in self.components:
                        self.components[id] = {'id': id}
                    a = self.code('div',{'class':'container-fluid d-flex flex-row p-0 m-0'},[view])
                    self.att(a,att)
                    #print('View:',view,'inner',inner)
                    return a
                else:
                    return view
            case 'Resource':
                return await self.compose_view('VideoMedia',text)
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
                    case 'submit':
                        button = self.code('button',{'class':'btn rounded-0','type':'submit','value':valor},inner)
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
                        obj =  self.code('iframe',{'src':url,'id':id,'style':'border:none;'},inner)
                        self.att(obj,att)
                        return obj
                    case 'modal':
                        btn_act = self.code('button',{'class':'btn btn-success'},[action.capitalize()])
                        self.att(btn_act,{'click':f"form(id:'form-{action}',action:'{action.lower()}')"})
                        form = self.code('form',{'id':f'form-{action}','action':'/'+action,'method':'POST'},inner)
                        # 'onclick':f'document.getElementById(\'form-{action}\').submit();'
                        return self.code('div',{'id':id,'class':'modal','data-bs-backdrop':'false'},[
                            self.code('div',{'class':f'modal-dialog modal-{size} modal-dialog-centered modal-dialog-scrollable'},[
                                self.code('div',{'class':'modal-content'},[
                                    self.code('div',{'class':'modal-header'}),
                                    self.code('div',{'class':'modal-body'},[form]),
                                    self.code('div',{'class':'modal-footer'},[
                                        self.code('button',{'class':'btn btn-secondary','data-bs-dismiss':'modal'},['Close']),
                                        btn_act
                                    ])
                                ]),
                            ]),
                        ])
            case 'Group':
                tipo = att['type'] if 'type' in att else 'None'
                match tipo:
                    case 'card':
                        r = self.code('div',{'class':'card-group'},inner)
                        self.att(r,att)
                        return r
                    case 'button':
                        gg = self.code('div',{'class':'btn-group'},inner)
                        self.att(gg,att)
                        return gg
                    case 'list':
                        new = []
                        for item in inner:
                            li = self.code('li',{'class':'list-group-item'},[item])
                            new.append(li)
                        ul = self.code('ul',{'class':'list-group'},new)
                        self.att(ul,att)
                        return ul
                    case 'pagination':
                        new = []
                        for item in inner:
                            li = self.code('li',{'class':'page-item'},[item])
                            new.append(li)
                        ul = self.code('ul',{'class':'pagination'},new)
                        self.att(ul,att)
                        return ul
                    case 'breadcrumb':
                        new = []
                        for item in inner:
                            li = self.code('li',{'class':'breadcrumb-item'},[item])
                            new.append(li)
                        ol = self.code('ol',{'class':'breadcrumb m-0'},new)
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

                        tab = self.code('details',{'class':'','open':'open'},[
                            self.code('summary',{'class':''},[inner[0]]),
                            self.code('ul',{'class':''},new)
                        ])
                        
                        self.att(tab,att)
                        return tab
                    case 'accordion':
                        accordion_id = att['id'] if 'id' in att else "accordionExample"
                        items = []
                        pair_index = 1  # per collapseOne, collapseTwo...

                        # Sicurezza: assicurati che inner abbia lunghezza pari
                        if len(inner) % 2 != 0:
                            inner = inner[:-1]  # Rimuove l'ultimo elemento orfano

                        for i in range(0, len(inner), 2):
                            header = inner[i]
                            body = inner[i + 1]

                            # Assicurati che non siano None
                            if header is None or body is None:
                                continue

                            collapse_id = f"collapse-{accordion_id}"
                            #collapse_id = accordion_id
                            
                            is_first = (pair_index == 1)

                            button = self.code('button', {
                                'class': 'accordion-button collapsed',
                                'type': 'button',
                                'data-bs-toggle': 'collapse',
                                'data-bs-target': f"#{collapse_id}",
                                'aria-expanded': 'false',
                                'aria-controls': collapse_id
                            }, [header])

                            header_h2 = self.code('h2', {'class': 'accordion-header'}, [button])
                            body_inner = self.code('div', {'class': 'accordion-body p-0 m-0'}, [body])
                            collapse_div = self.code('div', {
                                'id': collapse_id,
                                'class': 'accordion-collapse collapse',
                                'data-bs-parent': f"#{accordion_id}",
                            }, [body_inner])

                            accordion_item = self.code('div', {'class': 'accordion-item'}, [header_h2, collapse_div])
                            items.append(accordion_item)
                            pair_index += 1

                        accordion = self.code('div', {'class': 'accordion', 'id': accordion_id}, items)
                        self.att(accordion, att)
                        return accordion
                    case _:
                        return self.code('div',{'class':'container-fluid p-0 m-0'},inner)
            case 'Input':
                id = att['id'] if 'id' in att else str(uuid.uuid4())
                tipo = att['type'] if 'type' in att else 'None'
                tipi = ["button","checkbox","color","date","datetime-local","email","file","hidden","image","month","number","password","radio","range","reset","search","submit","tel","text","time","url","week"]
                valor = att['value'] if 'value' in att else ''
                if 'storekeeper' in data and 'storekeeper' in att:
                    if type(data['storekeeper']) == type(dict()):
                        valor = str(language.get(att['storekeeper'],data['storekeeper']))
                    else:
                        valor = str(data['storekeeper'])
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
                        if 'selected' in att and att['selected'] == 'true':
                            input = self.code('input',{'class':'form-check form-check-input','type':'checkbox','value':valor,'checked':'checked'})
                        else:
                            input = self.code('input',{'class':'form-check form-check-input','type':'checkbox','value':valor})
                        self.att(input,att)
                        return input
                    case 'textarea':
                        input = self.code('textarea',{'class':'form-control','rows':'3','placeholder':placeholder},inner)
                        self.att(input,att)
                        return input
                    case 'radio':
                        if 'selected' in att and att['selected'] == 'true':
                            input = self.code('input',{'class':'form-check form-check-input','type':'radio','value':valor,'checked':'checked'})
                        else:
                            input = self.code('input',{'class':'form-check form-check-input','type':'radio','value':valor})
                        self.att(input,att)
                        if inner and len(inner) > 0:
                            label = self.code('label',{'class':'btn','for':id},inner)
                            return self.code('div',{'class':''},[input,label])
                        return input
                    case 'switch':
                        input = self.code('input',{'class':'form-check form-switch form-check-input','type':'checkbox','role':'switch'})
                        self.att(input,att)
                        return input
                    case 'color':
                        input = self.code('input',{'class':'form-control form-control-color','type':'color','value':valor})
                        self.att(input,att)
                        return input
                    case 'range':
                        plus = {}
                        if 'min' in att:
                            plus['min'] = att['min']
                        if 'max' in att:
                            plus['max'] = att['max']
                        if 'step' in att:
                            plus['step'] = att['step']
                        input = self.code('input',{'class':'form-range','type':'range','value':valor}|plus)
                        self.att(input,att)
                        return input
                    case _:
                        input = self.code('input',{'class':'form-control','type':'text','value':valor,'placeholder':placeholder})
                        self.att(input,att)
                        return input
            case 'Text':
                #text-muted text-truncate
                tipo = att['type'] if 'type' in att else 'None'
                if 'storekeeper' in data and 'storekeeper' in att:
                    if type(data['storekeeper']) == type(dict()):
                        text = str(language.get(att['storekeeper'],data['storekeeper']))
                    else:
                        text = str(data['storekeeper'])
                    #print(att['storekeeper'],'text',data['storekeeper'])
                
                match tipo:
                    case 'editable':
                        if text:
                            text = escape(text)
                        text = self.code('div',{'contenteditable':'true'},text)
                        self.att(text,att)
                        return text
                    case 'code':
                        #if text:
                        #    text = escape(text)
                        code = self.code('code',{},[text])
                        pre = self.code('pre',{},[code])
                        self.att(pre,att)
                        return pre
                    case 'text':
                        if text:
                            text = escape(text)
                        obj = self.code('p',{'class':'fw-lighter p-0 m-0','type':'data'},text)
                        self.att(obj,att)
                        return obj
                    case 'data':
                        if text:
                            text = escape(text)
                        dt = datetime.fromisoformat(text)
                        text = dt.strftime('%Y-%m-%d %H:%M')
                        obj = self.code('p',{'class':'fw-lighter p-0 m-0','type':'data'},text)
                        self.att(obj,att)
                        return obj
                    case _:
                        if text:
                            text = escape(text)
                        inner.append(text)
                        obj = self.code('p',{'class':'text-truncate fw-lighter p-0 m-0','type':'data'},inner)
                        self.att(obj,att)
                        return obj
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
                
                if 'inner' in data:
                    data.pop('inner')
                if 'component' in data:
                    data.pop('component')
                
                xml_string = elements_to_xml_string(elements)
                url = f'application/view/component/{tag}.xml'
                #attrii = ''.join(x.outerHTML for x in att)
                id = att['id'] if 'id' in att else str(uuid.uuid1())
                if id not in self.components:
                    self.components[id] = {'id': id}
                    self.components[id]['view'] = f'application/view/component/{tag}.xml'
                    attributes = " ".join([f"{key}='{value}'" for key, value in att.items()])
                    self.components[id]['inner'] = f"<{tag} id='{id}' >{markupsafe.Markup(xml_string)}{data.get('code','')}</{tag}>"
                    self.components[id]['attributes'] = att
                    #self.components[id]['storekeeper'] = data.get('storekeeper',dict())

                inner = markupsafe.Markup(xml_string)+data.get('code','')
                if 'text' in data:
                    data.pop('text')
                    pass
                #await messenger.post(domain='debug',message=f"✅ Elemento: {tag}|{id} creato.")
                
                argg = data|{
                    'component':self.components.get(id,{}),
                    'url':url,
                    'inner':inner,
                }
                #print(att,data.get('storekeeper',{}).get('component',{}),id,tag,'DATA|COM',data)
                #print(att,data.get('storekeeper',{}).get('component',{}),id,tag,'DATA|arg',argg)
                # Creiamo la vista per il componente
                
                view = await self.builder(**argg)

                #view = await self.mount_view(root,data)

                self.att(view, att|{'component':tag})
                return view