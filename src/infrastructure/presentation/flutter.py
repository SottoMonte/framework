import flet as ft
import xml.etree.ElementTree as ET
import application.port.presentation as portPresentation
import application.service.flow as flow
import importlib
from jinja2 import Environment, PackageLoader, select_autoescape

def ATTR(root):
    setable = dict({})
    for key in root.attrib:
        if key != 'id':
            match str(key):
                case 'alignment':
                    somemodule = ft.MainAxisAlignment
                    icn = getattr(somemodule, root.attrib[key])
                    setable[key] = icn
                case 'icon_size': setable[key] = int(root.attrib[key])
                case 'on_click':
                    #print(globals())
                    #event = globals()[root.attrib[key]]
                    name_module,name_func = root.attrib[key].split('::',1)
                    #print('#',name_module,name_func)
                    module = importlib.import_module('application.plug.controller.'+name_module, package=None)
                    
                    func = getattr(module,name_func)
                    setable[key] = func
                case 'on_change':
                    name_module,name_func = root.attrib[key].split('::',1)
                    module = importlib.import_module('application.plug.controller.'+name_module, package=None)
                    func = getattr(module,name_func)
                    setable[key] = func
                case 'on_long_press':
                    name_module,name_func = root.attrib[key].split('::',1)
                    module = importlib.import_module('application.plug.controller.'+name_module, package=None)
                    func = getattr(module,name_func)
                    setable[key] = func
                case 'on_blur':
                    name_module,name_func = root.attrib[key].split('::',1)
                    module = importlib.import_module('application.plug.controller.'+name_module, package=None)
                    func = getattr(module,name_func)
                    setable[key] = func
                case 'on_submit':
                    name_module,name_func = root.attrib[key].split('::',1)
                    module = importlib.import_module('application.plug.controller.'+name_module, package=None)
                    func = getattr(module,name_func)
                    setable[key] = func
                case 'on_focus':
                    name_module,name_func = root.attrib[key].split('::',1)
                    module = importlib.import_module('application.plug.controller.'+name_module, package=None)
                    func = getattr(module,name_func)
                    setable[key] = func
                case 'icon':
                    somemodule = ft.icons
                    icn = getattr(somemodule, root.attrib[key])
                    setable[key] = icn
                case 'height':setable[key] = int(root.attrib[key])
                case 'thickness':setable[key] = int(root.attrib[key])
                case 'width':setable[key] = int(root.attrib[key])
                case 'spacing':setable[key] = int(root.attrib[key])
                case 'bgcolor':setable[key] = ft.colors.with_opacity(1, root.attrib[key])
                case 'color':setable[key] = ft.colors.with_opacity(1, root.attrib[key])
                case 'size':setable[key] = int(root.attrib[key])
                case 'margin':setable[key] = int(root.attrib[key])
                case 'padding':setable[key] = int(root.attrib[key])
                case 'border_radius':setable[key] = int(root.attrib[key])
                case 'spacing':setable[key] = int(root.attrib[key])
                case 'text_size':setable[key] = int(root.attrib[key])
                case 'label':setable[key] = root.attrib[key]
                case 'locator':
                    with open(root.attrib[key], mode="r") as file:
                            content = file.read()
                    setable['value'] = content
                case 'expand':
                    if root.attrib[key] == 'True': setable[key] = True
                    else: setable[key] = int(root.attrib[key])
                case _:setable[key] = root.attrib[key]
    return setable

class adapter(portPresentation.presentation):

    def __init__(self,**constants):
        self.tree_view = dict()
        self.env = Environment()
        self.config = constants['config'] 

    @flow.async_function(ports=('storekeeper',))
    async def builder(self,worker,file,data,storekeeper,**constants):
        stri = await storekeeper.get(model="file",file=file,value={'file':file})
        #tree = ET.parse(file)
        template = self.env.from_string(stri['result']['file'])
        rresult = template.render(**data)

        tree = ET.ElementTree(ET.fromstring(rresult))

        root = tree.getroot()

        def mount_view(root):
            
            #print(id(self.tree_view))
            inn = []
            if len(root) > 0:
                for x in root:
                    #constants['messenger'].post(message=f"Tag:{x.tag}, Attribute:{x.attrib}, Length:{len(x)}",type='debug')
                    ffff = mount_view(x)
                    inn.append(ffff)

            match root.tag:
                case 'If':
                    if '@' not in root.attrib['view']:
                        with open(root.attrib['view'], mode="r") as file:
                            content = file.read()
                        tree1 = ET.ElementTree(ET.fromstring(content))
                        root1 = tree1.getroot()
                        return mount_view(root1)
                    else:
                        return ft.Text(root.attrib['view'])
                case 'ForEach':
                    doubled = []
                    def deep(deep_data):
                        deep_inn = []
                        if 'dir' in deep_data:
                            for x in deep_data[3]:
                                 deep_inn.append(deep(x))
                            return deep_inn
                        else:
                            for placeholder in deep_data:
                                for item in inn:
                                    itt = ft.TextButton(text=item.text,tooltip=item.tooltip)
                                    if item.text.startswith('@'):
                                        #print(item)
                                        
                                        itt.text = placeholder[2]
                                        itt.tooltip = placeholder[1]
                                        itt.on_long_press = item.on_long_press
                                        #itt.on_long_press = ATTR({'on_long_press':'open_file'})
                                    
                                    deep_inn.append(itt)
                            return deep_inn
                    
                    if root.attrib['recursive'] == 'True':
                        return ft.ListView(controls=deep(data[0]))
                    else:
                        for placeholder in data:
                            for item in inn:
                                itt = ft.TextButton(text=item.text,tooltip=item.tooltip)
                                if item.text.startswith('@'):
                                    #print(item)
                                    
                                    itt.text = placeholder[2]
                                    itt.tooltip = placeholder[1]
                                    itt.on_long_press = item.on_long_press
                                    #itt.on_long_press = ATTR({'on_long_press':'open_file'})
                                
                                doubled.append(itt)
                    
                    return ft.ListView(controls=doubled)
                case 'Locator':
                    if '@' not in root.attrib['view']:
                        with open('src/domain/view/'+root.attrib['view'], mode="r") as file:
                            content = file.read()

                        t = self.env.from_string(content)
                        result = t.render(**data)
                        tree1 = ET.ElementTree(ET.fromstring(result))
                        root1 = tree1.getroot()
                        #print(await constants['locator'](module='/home/asd/accent/src/domain/views/'+root.attrib['view']))
                        return mount_view(root1)
                    else:
                        return ft.Text(root.attrib['view'])
                case 'Container':
                    setable = ATTR(root)
                    #ft.Column(inn,expand=True)
                    if len(inn) == 1:
                        item = ft.Container(content=inn[0],**setable)
                    else:
                        item = ft.Container(**setable)
                    if 'id' in root.attrib and (not root.attrib['id'] in self.tree_view):
                        self.tree_view[root.attrib['id']] = item
                        return self.tree_view[root.attrib['id']]
                    else:return item
                case 'Text':
                    setable = ATTR(root)
                    item = ft.Text(root.text,**setable)

                    if 'id' in root.attrib and (not root.attrib['id'] in self.tree_view):
                        self.tree_view[root.attrib['id']] = item
                        return self.tree_view[root.attrib['id']]
                    else:return item
                case 'Column':
                    setable = ATTR(root)
                    item = ft.Column(controls=inn,**setable)
                    if 'id' in root.attrib and (not root.attrib['id'] in self.tree_view):
                        self.tree_view[root.attrib['id']] = item
                        return self.tree_view[root.attrib['id']]
                    else:return item
                case 'Row':
                    setable = ATTR(root)
                    item = ft.Row(controls=inn,**setable)
                    if 'id' in root.attrib and (not root.attrib['id'] in self.tree_view):
                        self.tree_view[root.attrib['id']] = item
                        return self.tree_view[root.attrib['id']]
                    else:return item
                case 'IconButton': 
                    setable = ATTR(root)
                    #on_click=event
                    item = ft.IconButton(**setable)
                    if 'id' in root.attrib and (not root.attrib['id'] in self.tree_view):
                        self.tree_view[root.attrib['id']] = item
                        return self.tree_view[root.attrib['id']]
                    else:return item
                case 'TextButton': 
                    setable = ATTR(root)
                    #on_click=event
                    item = ft.TextButton(**setable)
                    if 'id' in root.attrib and (not root.attrib['id'] in self.tree_view):
                        self.tree_view[root.attrib['id']] = item
                        return self.tree_view[root.attrib['id']]
                    else:return item
                case 'TextField': 
                    setable = ATTR(root)
                    item = ft.TextField(**setable)
                    if 'id' in root.attrib and (not root.attrib['id'] in self.tree_view):
                        self.tree_view[root.attrib['id']] = item
                        return self.tree_view[root.attrib['id']]
                    else:return item
                case 'Dropdown': 
                    setable = ATTR(root)
                    item = ft.Dropdown(options=inn,**setable)
                    if 'id' in root.attrib and (not root.attrib['id'] in self.tree_view):
                        self.tree_view[root.attrib['id']] = item
                        return self.tree_view[root.attrib['id']]
                    else:return item
                case 'DropdownOption': 
                    return ft.dropdown.Option(root.text)
                case 'WindowDragArea':
                    setable = ATTR(root)
                    item = ft.WindowDragArea(content=ft.ListView(inn,expand=True),maximizable=False,**setable)
                    if 'id' in root.attrib and (not root.attrib['id'] in self.tree_view):
                        self.tree_view[root.attrib['id']] = item
                        return self.tree_view[root.attrib['id']]
                    else:return item
                case 'NavigationRail':
                    setable = ATTR(root)
                    item = ft.NavigationRail(destinations=inn,**setable)
                    if 'id' in root.attrib and (not root.attrib['id'] in self.tree_view):
                        self.tree_view[root.attrib['id']] = item
                        return self.tree_view[root.attrib['id']]
                    else:return item
                case 'Tabs':
                    setable = ATTR(root)
                    item = ft.Tabs(tabs=inn, **setable)
                    if 'id' in root.attrib and (not root.attrib['id'] in self.tree_view):
                        self.tree_view[root.attrib['id']] = item
                        return self.tree_view[root.attrib['id']]
                    else:return item
                case 'Tab':
                    setable = ATTR(root)
                    item = ft.Tab(content=ft.Column(inn,expand=True),**setable)
                    if 'id' in root.attrib and (not root.attrib['id'] in self.tree_view):
                        self.tree_view[root.attrib['id']] = item
                        return self.tree_view[root.attrib['id']]
                    else:return item
                case 'Stack':
                    setable = ATTR(root)
                    item = ft.Stack(controls=inn,**setable)
                    if 'id' in root.attrib and (not root.attrib['id'] in self.tree_view):
                        self.tree_view[root.attrib['id']] = item
                        return self.tree_view[root.attrib['id']]
                    else:return item
                case 'ListView':
                    setable = ATTR(root)
                    item = ft.ListView(controls=inn,**setable)
                    if 'id' in root.attrib and (not root.attrib['id'] in self.tree_view):
                        self.tree_view[root.attrib['id']] = item
                        return self.tree_view[root.attrib['id']]
                    else:return item
                case 'Divider':
                    setable = ATTR(root)
                    item = ft.Divider(**setable)
                    if 'id' in root.attrib and (not root.attrib['id'] in self.tree_view):
                        self.tree_view[root.attrib['id']] = item
                        return self.tree_view[root.attrib['id']]
                    else:return item
                case 'DataTable':
                    setable = ATTR(root)
                    c = [element for element in inn if isinstance(element,ft.DataColumn)]
                    r = [element for element in inn if isinstance(element,ft.DataRow)]
                    #print(c,r)
                    item = ft.DataTable(columns=c,rows=r,**setable)
                    if 'id' in root.attrib and (not root.attrib['id'] in self.tree_view):
                        self.tree_view[root.attrib['id']] = item
                        return self.tree_view[root.attrib['id']]
                    else:return item
                case 'DataColumn':
                    setable = ATTR(root)
                    item = ft.DataColumn(inn[0],**setable)
                    if 'id' in root.attrib and (not root.attrib['id'] in self.tree_view):
                        self.tree_view[root.attrib['id']] = item
                        return self.tree_view[root.attrib['id']]
                    else:return item
                case 'DataRow':
                    setable = ATTR(root)
                    item = ft.DataRow(inn,**setable)
                    if 'id' in root.attrib and (not root.attrib['id'] in self.tree_view):
                        self.tree_view[root.attrib['id']] = item
                        return self.tree_view[root.attrib['id']]
                    else:return item
                case 'DataCell':
                    setable = ATTR(root)
                    item = ft.DataCell(inn[0],**setable)
                    if 'id' in root.attrib and (not root.attrib['id'] in self.tree_view):
                        self.tree_view[root.attrib['id']] = item
                        return self.tree_view[root.attrib['id']]
                    else:return item
                case 'ExpansionTile':
                    setable = ATTR(root)
                    item = ft.ExpansionTile(title=ft.Text("ExpansionTile 1"))
                    if 'id' in root.attrib and (not root.attrib['id'] in self.tree_view):
                        self.tree_view[root.attrib['id']] = item
                        return self.tree_view[root.attrib['id']]
                    else:return item
                case 'ExpansionPanel':
                    setable = ATTR(root)
                    item = ft.ExpansionPanel(header=ft.ListTile(title=ft.Text("1")),)
                    if 'id' in root.attrib and (not root.attrib['id'] in self.tree_view):
                        self.tree_view[root.attrib['id']] = item
                        return self.tree_view[root.attrib['id']]
                    else:return item
                case 'VerticalDivider':
                    setable = ATTR(root)
                    item = ft.VerticalDivider()
                    if 'id' in root.attrib and (not root.attrib['id'] in self.tree_view):
                        self.tree_view[root.attrib['id']] = item
                        return self.tree_view[root.attrib['id']]
                    else:return item
                case 'ListTile':
                    setable = ATTR(root)
                    item = ft.ListTile(
                            title=ft.Text("One-line with trailing control"),
                            trailing=ft.PopupMenuButton(
                                icon=ft.icons.MORE_VERT,
                                items=[
                                    ft.PopupMenuItem(text="Item 1"),
                                    ft.PopupMenuItem(text="Item 2"),
                                ],
                            ),
                        )
                    if 'id' in root.attrib and (not root.attrib['id'] in self.tree_view):
                        self.tree_view[root.attrib['id']] = item
                        return self.tree_view[root.attrib['id']]
                    else:return item

        return mount_view(root)

    def loader(self, *services, **constants):
        async def main(page: ft.Page):
            page.window_title_bar_hidden = True
            page.window_title_bar_buttons_hidden = True
            page.title = self.config['title']
            page.vertical_alignment = ft.MainAxisAlignment.CENTER
            page.spacing = 0
            page.margin=0
            page.padding=0
            
            view = await self.builder("null",self.config['dir'],dict())
            await page.add_async(view,)
        ft.app(main)