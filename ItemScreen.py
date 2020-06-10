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
            left_action_items : [['arrow-left', lambda x : root.go_back()]]
    
        MDGridLayout:
            cols:1
            id : ItemGrid
"""

class ItemCard(Base):

    on_release = None

    __tablename__ = "Articulos"

    internalId = Column(Integer,primary_key=True)
    Code = Column(String)
    Name = Column(String)
    Closed = Column(Integer)
    Price = Column(Float)
    Category = Column(String)
    Recipe = Column(Integer)
    RecipeContent = Column(String)
    
    def load_widget(self):
        from TableScreen import BlueCenteredLabel
        self.Card = MDCard(size_hint_y=None,height=Window.height/3.6)#, padding=(20,20,20,5))
        box = MDBoxLayout(orientation="vertical")#, spacing=5)
        box.add_widget(BlueCenteredLabel(font_style="H3",padding=(1,1),size_hint_y=.2,text=self.Code))
        # box.add_widget(BlueCenteredLabel(font_style="Subtitle1",padding=(1,1),size_hint_y=.2,text=self.Name))
        box.add_widget(BlueCenteredLabel(font_style="H3",padding=(1,1),size_hint_y=.2,text="Precio: $%s" % self.Price))
        self.Card.add_widget(box)
        self.Card.on_release=lambda : self.on_release(self)
        return self.Card

class CategoryCard(Base):
    
    __tablename__ = "Categorias"

    internalId = Column(Integer,primary_key=True)
    Code = Column(String)
    # Name = Column(String)    
    Image = Column(String)

    on_release = None

    def load_widget(self):
        from TableScreen import BlueCenteredLabel
        self.Card = MDCard(size_hint_y=None,height=Window.height/3.6, padding=(20,20,20,5))
        box = MDBoxLayout(orientation="vertical", spacing=5)
        image = AsyncImage(source=self.Image,keep_ratio = False, allow_stretch = True)
        box.add_widget(image)
        box.add_widget(BlueCenteredLabel(font_style="H3",padding=(1,1),size_hint_y=.2,text=self.Code))
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
                    cols = 2, padding=(30,30,30,30), spacing=20)

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
                cols = 3, padding=(30,30,30,30), spacing=20)

            for i in res:
                c = i.load_widget()
                grid.add_widget(c)

            self.ids.ItemGrid.add_widget(grid)
            self.ids.ItemToolbar.title = card.Code

    def go_back(self):
        if self.ids.ItemToolbar.title == "Categorias":
            self.parent.current = "TablePage" 
            return
        self.load_categories()

