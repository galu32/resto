from Libs import *
from SM import Base, _session
from BaseScreen import *

itemscreen_kv = """
<ItemPage>:
    name : "ItemPage"
    
    MDGridLayout:
        cols:1
        id : MainGrid

        MDToolbar:
            id : ItemToolbar
            pos_hint : {"top" : 1}
            left_action_items : [['chef-hat', lambda x : nav_drawer.toggle_nav_drawer()]]
            right_action_items : [['plus', lambda x : root.new_record()]]
    
        MDGridLayout:
            cols:1
            id : ItemGrid



    MDNavigationDrawer:
        id: nav_drawer

        MDGridLayout:
            cols : 1

            MDToolbar:
                pos_hint : {"top" : 1}
                right_action_items : [['close', lambda x : nav_drawer.toggle_nav_drawer()]]

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

class ItemCard(Base):
    
    __tablename__ = "Articulos"

    internalId = Column(Integer,primary_key=True)
    Code = Column(String)
    Name = Column(String)
    Closed = Column(Integer)
    Price = Column(Float)
    Category = Column(String)

    def load_widget(self):
        from TableScreen import BlueCenteredLabel
        self.Card = MDCard(size_hint_y=None,height=Window.height/3.6, padding=(20,20,20,5))
        box = MDBoxLayout(orientation="vertical", spacing=5)
        box.add_widget(BlueCenteredLabel(font_style="H3",padding=(1,1),size_hint_y=.2,text="Codigo: %s"%self.Code))
        box.add_widget(BlueCenteredLabel(font_style="Subtitle1",padding=(1,1),size_hint_y=.2,text=self.Name))
        box.add_widget(BlueCenteredLabel(font_style="Subtitle2",padding=(1,1),size_hint_y=.2,text="Precio: $%s" % self.Price))
        self.Card.add_widget(box)
        # self.Card.on_release=self.open_category
        return self.Card

class CategoryCard(Base):
    
    __tablename__ = "Category"

    internalId = Column(Integer,primary_key=True)
    Code = Column(String)
    Name = Column(String)    
    Image = Column(String)

    on_release = None

    def load_widget(self):
        from TableScreen import BlueCenteredLabel
        self.Card = MDCard(size_hint_y=None,height=Window.height/3.6, padding=(20,20,20,5))
        box = MDBoxLayout(orientation="vertical", spacing=5)
        image = AsyncImage(source=self.Image,keep_ratio = False, allow_stretch = True)
        box.add_widget(image)
        box.add_widget(BlueCenteredLabel(font_style="H3",padding=(1,1),size_hint_y=.2,text=self.Name))
        self.Card.add_widget(box)
        self.Card.on_release=self.open_category
        return self.Card

    def open_category(self):
        self.on_release(self)

class ItemPage(BasePage):

    Builder.load_string(itemscreen_kv)
    
    def __init__(self,**kwargs):
        super(ItemPage,self).__init__(**kwargs)

    def load_categories(self):
        se = _session()
        res = se.query(CategoryCard)
        if res.count():
            self.ids.ItemGrid.clear_widgets()
            grid = MDGridLayout(
                    cols = 2, padding=(30,30,30,30), spacing=20)#,size_hint_y=None, height=)
            # scroll = ScrollView(size_hint_y=None,height=grid.height)
            # scroll.add_widget(grid)
            for c in res:
                card = c.load_widget()
                c.on_release = lambda x :self.open_category(x)
                grid.add_widget(card)

            self.ids.ItemGrid.add_widget(grid)
            self.ids.ItemToolbar.title = "Categorias"
        se.close()

    def open_category(self,card):
        se = _session()
        res = se.query(ItemCard).filter(ItemCard.Category == card.Code)
        if res.count():
            self.ids.ItemGrid.clear_widgets()
            grid = MDGridLayout(
                cols = 3, padding=(30,30,30,30), spacing=20)#,size_hint_y=None, height=)

            for i in res:
                c = i.load_widget()
                grid.add_widget(c)

            self.ids.ItemGrid.add_widget(grid)
            self.ids.ItemToolbar.title = card.Name

    def new_record(self):
        if self.ids.ItemToolbar.title == "Categorias":
            content = MDGridLayout(cols=1, spacing=5,padding=(10,10,10,10),md_bg_color=[1,1,1,1])#,orientation="vertical")
            text1 = MDTextField()
            text1.hint_text = "Codigo..."
            text2 = MDTextField()
            text2.hint_text = "Nombre..."
            text3 = MDTextField()
            text3.hint_text = "Url Imagen..."
            b1 = MDRaisedButton(
                        text="Cancelar", on_release=lambda x: self.new_record_ask(False),
                        pos_hint = {"center_x": .5, "center_y": .5}
                    )
            b2 = MDRaisedButton(
                        text="Aceptar", on_release=lambda x: self.new_record_ask(True),
                        pos_hint = {"center_x": .5, "center_y": .5}
                    )
            bbox = MDGridLayout(cols=2,spacing=30,padding=(10,10,10,0))
            content.add_widget(text1)
            content.add_widget(text2)
            content.add_widget(text3)
            bbox.add_widget(b1)
            bbox.add_widget(b2)
            content.add_widget(bbox)

            self.new_rec = ModalView(auto_dismiss=False,size = content.size, size_hint=(.4,.4))
            self.new_rec.add_widget(content)
            self.new_rec.open()

    def new_record_ask(self,value):
        if not value: return self.new_rec.dismiss()