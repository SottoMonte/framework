import flet as ft
import flet_video as fv
import importlib
import asyncio

modules = {'flow': 'framework.service.flow','presentation': 'framework.port.presentation'}

class adapter(presentation.port):
    @staticmethod
    async def attribute_id(widget, pr, value): widget.id = value

    @staticmethod
    async def attribute_name(widget, pr, value): widget.name = value

    @staticmethod
    async def attribute_tooltip(widget, pr, value): widget.tooltip = value

    @staticmethod
    async def attribute_placeholder(widget, pr, value): widget.hint_text = value

    @staticmethod
    async def attribute_value(widget, pr, value): widget.value = value

    @staticmethod
    async def attribute_state(widget, pr, value):
        if value == "readonly":
            widget.read_only = True
        elif value == "disabled":
            widget.disabled = True
        elif value == "selected":
            widget.selected = True
        elif value == "enabled":
            widget.enabled = True

    @flow.asynchronous(managers=('executor',))
    @staticmethod
    async def attribute_click(self,widget, pr, value,executor):
        async def on_click(e):
            await executor.act(action=value)
        
        widget.on_click = on_click

    @staticmethod
    async def attribute_change(widget, pr, value): widget.on_change = value

    @staticmethod
    async def attribute_route(widget, pr, value): widget.route = value

    @staticmethod
    async def attribute_init(widget, pr, value): widget.on_init = value

    @staticmethod
    async def attribute_width(widget, pr, value): widget.width = int(value)

    @staticmethod
    async def attribute_height(widget, pr, value): widget.height = int(value)

    @staticmethod
    async def attribute_space(widget, pr, value): widget.space = value

    @staticmethod
    async def attribute_expand(widget, pr, value):
        if value == "fill":
            widget.expand = True
        elif value == "vertical":
            widget.height = ft.MainAxisSize.MAX
        elif value == "horizontal":
            widget.width = ft.MainAxisSize.MAX
        else:
            widget.expand = False

    @staticmethod
    async def attribute_collapse(widget, pr, value): widget.collapse = value

    @staticmethod
    async def attribute_border(widget, pr, value): widget.border = value

    @staticmethod
    async def attribute_border_top(widget, pr, value): widget.border_top = value

    @staticmethod
    async def attribute_border_bottom(widget, pr, value): widget.border_bottom = value

    @staticmethod
    async def attribute_border_left(widget, pr, value): widget.border_left = value

    @staticmethod
    async def attribute_border_right(widget, pr, value): widget.border_right = value

    @staticmethod
    async def attribute_margin(widget, pr, value): widget.margin = value

    @staticmethod
    async def attribute_margin_top(widget, pr, value): widget.margin_top = value

    @staticmethod
    async def attribute_margin_bottom(widget, pr, value): widget.margin_bottom = value

    @staticmethod
    async def attribute_margin_left(widget, pr, value): widget.margin_left = value

    @staticmethod
    async def attribute_margin_right(widget, pr, value): widget.margin_right = value

    @staticmethod
    async def attribute_padding(widget, pr, value): widget.padding = int(value)

    @staticmethod
    async def attribute_padding_top(widget, pr, value): widget.padding_top = value

    @staticmethod
    async def attribute_padding_bottom(widget, pr, value): widget.padding_bottom = value

    @staticmethod
    async def attribute_padding_left(widget, pr, value): widget.padding_left = value

    @staticmethod
    async def attribute_padding_right(widget, pr, value): widget.padding_right = value

    @staticmethod
    async def attribute_size(widget, pr, value): widget.size = value

    @staticmethod
    async def attribute_alignment_horizontal(widget, pr, value): widget.alignment_horizontal = value

    @staticmethod
    async def attribute_alignment_vertical(widget, pr, value): widget.alignment_vertical = value

    @staticmethod
    async def attribute_alignment_content(widget, pr, value): widget.alignment_content = value

    @staticmethod
    async def attribute_position(widget, pr, value): widget.position = value

    @staticmethod
    async def attribute_style(widget, pr, value): widget.style = value

    @staticmethod
    async def attribute_shadow(widget, pr, value): widget.shadow = value

    @staticmethod
    async def attribute_opacity(widget, pr, value): widget.opacity = float(value)

    @staticmethod
    async def attribute_background_color(widget, pr, value): widget.bgcolor = value

    @staticmethod
    async def attribute_class(widget, pr, value): widget.class_name = value  # "class" is reserved


    # Mappa dei costruttori data-driven
    '''widget_map = {
        'Button': lambda inner, props: (
            lambda variant: {
                'icon': ft.IconButton(
                    icon=props.get('icon', ft.icons.PLAY_ARROW),
                    icon_size=props.get('icon_size', 24),
                    on_click=props.get('on_click'),
                    tooltip=props.get('tooltip', "Play"),
                    **props
                ),
                'text': ft.TextButton(
                    text=props.get('text', "Click Me"),
                    on_click=props.get('on_click'),
                    tooltip=props.get('tooltip', "Click to perform an action"),
                    **props
                ),
            }.get(variant, ft.TextButton(text="Default", **props))
        )(props.get('variant', 'text')),
        'Video': lambda inner, props: fv.Video(
            expand=props.get('expand', True),
            playlist=inner,
            playlist_mode=props.get('playlist_mode', ft.PlaylistMode.LOOP),
            fill_color=props.get('fill_color', ft.Colors.BLUE_400),
            aspect_ratio=props.get('aspect_ratio', 16 / 9),
            volume=props.get('volume', 100),
            autoplay=props.get('autoplay', True),
            filter_quality=props.get('filter_quality', ft.FilterQuality.HIGH),
            muted=props.get('muted', False),
            on_loaded=props.get('on_loaded', lambda e: print("Video loaded successfully!")),
            on_enter_fullscreen=props.get('on_enter_fullscreen', lambda e: print("Video entered fullscreen!")),
            on_exit_fullscreen=props.get('on_exit_fullscreen', lambda e: print("Video exited fullscreen!")),
        ),
        'VideoMedia': lambda inner, props: fv.VideoMedia(inner),
        'Container': lambda inner, props: ft.Container(
            content=inner,
            expand=props.get('expand', True),
            bgcolor=props.get('bgcolor', ft.colors.with_opacity(1, 'white')),
            border_radius=props.get('border_radius', 10),
            padding=props.get('padding', 10),
            margin=props.get('margin', 10)
        ),
        'Text': lambda inner, props: ft.Text(inner, **props),
        'Column': lambda inner, props: ft.Column(controls=inner, **props),
        'Row': lambda inner, props: ft.Row(
            controls=inner,
            expand=props.get('expand', True),
            alignment=props.get('alignment', ft.MainAxisAlignment.CENTER),
            spacing=props.get('spacing', 10)
        ),
        'IconButton': lambda inner, props: ft.IconButton(
            icon=props.get('icon', ft.icons.PLAY_ARROW),
            icon_size=props.get('icon_size', 24),
            on_click=props.get('on_click', lambda e: print("Icon button clicked!")),
            tooltip=props.get('tooltip', "Play")
        ),
        'TextButton': lambda inner, props: ft.TextButton(
            text=props.get('text', "Click Me"),
            on_click=props.get('on_click', lambda e: print("Text button clicked!")),
            tooltip=props.get('tooltip', "Click to perform an action")
        ),
        'TextField': lambda inner, props: ft.TextField(
            label=props.get('label', "Enter text"),
            on_change=props.get('on_change', lambda e: print("Text field changed:", e.control.value)),
            on_submit=props.get('on_submit', lambda e: print("Text submitted:", e.control.value))
        ),
        'Dropdown': lambda inner, props: ft.Dropdown(
            options=inner,
            label=props.get('label', "Select an option"),
            on_change=props.get('on_change', lambda e: print("Dropdown changed:", e.control.value))
        ),
        'DropdownOption': lambda inner, props: ft.dropdown.Option(inner),
        'WindowDragArea': lambda inner, props: ft.WindowDragArea(
            content=ft.ListView(inner, expand=True),
            maximizable=props.get('maximizable', False),
            bgcolor=props.get('bgcolor', ft.colors.with_opacity(1, 'white')),
            border_radius=props.get('border_radius', 10),
            padding=props.get('padding', 10),
            margin=props.get('margin', 10)
        ),
        'NavigationRail': lambda inner, props: ft.NavigationRail(
            destinations=inner,
            selected_index=props.get('selected_index', 0),
            on_change=props.get('on_change', lambda e: print("Navigation rail changed:", e.control.selected_index)),
            bgcolor=props.get('bgcolor', ft.colors.with_opacity(1, 'white')),
            elevation=props.get('elevation', 4)
        ),
        'Tabs': lambda inner, props: ft.Tabs(
            tabs=inner,
            selected_index=props.get('selected_index', 0),
            on_change=props.get('on_change', lambda e: print("Tab changed:", e.control.selected_index)),
            expand=props.get('expand', True)
        ),
        'Tab': lambda inner, props: ft.Tab(
            content=ft.Column(inner, expand=True),
            text=props.get('text', "Tab Title"),
            icon=props.get('icon', ft.icons.TAB)
        ),
        'Stack': lambda inner, props: ft.Stack(
            controls=inner,
            expand=props.get('expand', True),
            alignment=props.get('alignment', ft.alignment.center)
        ),
        'List': lambda inner, props: ft.ListView(
            controls=inner,
            expand=props.get('expand', True),
            spacing=props.get('spacing', 10),
            padding=props.get('padding', 10)
        ),
        'Divider': lambda inner, props: ft.Divider(
            thickness=props.get('thickness', 1),
            color=props.get('color', ft.colors.with_opacity(1, 'grey')),
            padding=props.get('padding', 10)
        ),
    }'''

    def __init__(self,**constants):
        self.tree_view = dict()
        self.config = constants['config']
        
        self.initialize()
        async def main(page: ft.Page):
            #page.window_title_bar_hidden = True
            #page.window_title_bar_buttons_hidden = True
            #page.title = self.config['title']
            aaa = await self.host({'url':self.config.get('view')})
            
            page.vertical_alignment = ft.MainAxisAlignment.CENTER
            page.spacing = 0
            page.margin=0
            page.padding=0
            #print(self.builder)
            view = await self.builder(text=aaa)
            #print('VIEW',view)
            #await page.add_async(view,)
            page.add(view)
        asyncio.create_task(ft.app_async(main))

    @staticmethod
    def widget_button(inner, props):
        variant = props.get("variant", "text")
        if variant == "icon":
            return ft.IconButton(
                icon=props.get("icon", ft.icons.PLAY_ARROW),
                icon_size=props.get("icon_size", 24),
                on_click=props.get("on_click"),
            )
        return ft.TextButton(
            text=props.get("text", "Click Me"),
            on_click=props.get("on_click"),
        )

    @staticmethod
    def widget_video(inner, props):
        return fv.Video(playlist=inner)

    @staticmethod
    def widget_videomedia(inner, props):
        return fv.VideoMedia(inner)
    
    @staticmethod
    def widget_column(inner, props):
        print(inner)
        return ft.Column(controls=inner)
    
    @staticmethod
    def widget_row(inner, props):
        print('Row',inner)
        return ft.Row(controls=inner)
    
    @staticmethod
    def widget_container(inner, props):
        print('Container',inner,props)
        return ft.Container(content=ft.ResponsiveRow(expand=True,controls=inner))
    
    @staticmethod
    def widget_button(inner, props):
        print('Button',inner)
        return ft.FilledButton(content=ft.ResponsiveRow(expand=True,controls=inner))
    
    @staticmethod
    def widget_text(inner, props):
        print('Text',inner)
        text = ''
        for x in inner:
            if type(x) == type(''):
                text += x
                inner.remove(x)

        return ft.Text(value=text)
    
    @staticmethod
    def widget_input(inner, props):
        print('Input',inner,props)
        ttype = props.get('type','text')
        match ttype:
            case 'text':
                return ft.TextField()
            case 'password':
                return ft.TextField(password=True, can_reveal_password=True)
            case _:
                return ft.TextField()
    
    
    async def mount_route(self, *services, **constants):
        pass

    
    async def render_view(self, *services, **constants):
        pass

    
    async def mount_css(self, *services, **constants):
        pass