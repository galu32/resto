from Libs import * 
from SM import _session, Base
from TableScreen import BlueCenteredLabel

GT_kv = """
<NavDrawer>:
    orientation : "vertical"

    MDGridLayout:
        id : NavGrid
        cols : 1
        orientation : "vertical"

        MDToolbar:
            pos_hint : {"top" : 1}
            right_action_items : [['close', lambda x : root.toggle_nav_drawer()]]

        NavItem:
            text : "Mesas"
            icon : "table-chair"
        NavItem:
            text : "Articulos"
            icon : "food"
        NavItem:
            text : "Reportes"
            icon : "book-information-variant"
        NavItem:
            text : "Configuraciones"
            icon : "database-settings"

"""
Builder.load_string(GT_kv)

class Field(MDTextField):
    def __init__(self,**kwargs):
        super(Field,self).__init__(**kwargs)

class NavDrawer(MDNavigationDrawer):

    _current_user = ObjectProperty()

    def __init__(self,**kwargs):
        super(NavDrawer,self).__init__(**kwargs)

    def on__current_user(self,x,value):
        if not value: return self.remove_widget(self.children[0])
        card = MDCard(size_hint_y=.3)#size_hint=(None,None))
        box = MDGridLayout(padding=(2,2,2,2),cols=1)
        name = BlueCenteredLabel(text=self._current_user.Name,font_style="H6")
        name2 = BlueCenteredLabel(text="Administrador: %s" % ("Si" if self._current_user.Admin else "No"),font_style="H6")
        name3 = BlueCenteredLabel(text="",font_style="H6")
        b1 = MDRaisedButton(
                    text="Cambiar Contraseña", on_release=lambda x: print(x),
                    pos_hint = {"center_x": .5, "center_y": .5}
                )
        b2 = MDRaisedButton(
                    text="Salir", on_release=lambda x: self.logout(),
                    pos_hint = {"center_x": .5, "center_y": .5}
                )
        bbox = MDGridLayout(cols=2,spacing=30,padding=(2,2,2,2))
        bbox.add_widget(b1)
        bbox.add_widget(b2)
        box.add_widget(name)
        box.add_widget(name2)
        box.add_widget(name3)
        box.add_widget(bbox)
        card.add_widget(box)
        self.add_widget(card)

    def logout(self):
        self._current_user = 0
        self.parent.logout()