from Libs import *
from SM import _session, Base

basescreen_kv = """     
##basescreen

<Working>:
    canvas.before:
        PushMatrix
        Rotate:
            angle: root.angle
            axis: 0, 0, 1
            origin: root.center
    canvas.after:
        PopMatrix


    Image:
        # color : 1,0,0,1
        source: "images/icon.png"
        size_hint: None, None
        size: 150, 150
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}

"""
class Working(FloatLayout):

    angle = NumericProperty(0)

    def __init__(self, **kwargs):
        super(Working, self).__init__(**kwargs)
        anim = Animation(angle = 360, duration=2) 
        anim += Animation(angle = 360, duration=2)
        anim.repeat = True
        anim.start(self)

    def on_angle(self, item, angle):
        if angle == 360:
            item.angle = 0

class BasePage(Screen):

    Builder.load_string(basescreen_kv)
    working = BooleanProperty(defaultvalue=False)

    def __init__(self,**kwargs):
        super(BasePage,self).__init__(**kwargs)

    def on_working(self,screen,value):
        if value:
            self.add_widget(Working())
        else:
            self.remove_widget(self.children[0])

    def ErrorResponse(self,text=""):
        self.working = False
        if not text: text = "A ocurrido un error vuelve a intentarlo."
        Snackbar(text = text).show()

    def screen_switcher(self,screen):
        if screen == "Articulos":
            self.parent.current = "ItemPage"
            self.parent.ItemScreen.load_categories()
        if screen == "Mesas":
            self.parent.current = "TablePage"
        if screen == "Configuraciones":
            if not self.parent._current_user:
                return self.parent.login_dialog()
            if not self.parent._current_user.Admin:
                return Snackbar(text="Su usuario no tiene acceso a las Configuraciones.").show()
            self.parent.current = "ConfigPage"
        self.ids.nav_drawer.toggle_nav_drawer()

    def logout(self):
        self.parent._current_user = 0