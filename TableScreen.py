from Libs import *
from BaseScreen import *

tablescreen_kv = """     

<NavItem@OneLineAvatarIconListItem>:
    theme_text_color : "Custom"
    text_color : rgba("#2196F3")
    icon : ""
    on_release: root.parent.parent.parent.screen_switcher(root.text)

    IconLeftWidget:
        icon : root.icon
        theme_text_color : "Custom"
        text_color : rgba("#2196F3")

<TablePage>:

    name : "TablePage"

    MDGridLayout:
        cols : 1

        MDToolbar:
            id : BaseToolbar
            pos_hint : {"top" : 1}
            left_action_items : [['chef-hat', lambda x : nav_drawer.toggle_nav_drawer()]]
            MDRaisedButton :
                pos_hint : {"center_x": .5, "center_y": .5}
                text : "Cargar/Refrescar Mesas"
                on_release: root.load_tables()

        ScrollView:
            size_hint_y : None
            height : root.height

            MDGridLayout:
                id : TableGrid
                cols : 3
                padding : 10,10,10,10
                spacing : 5
                size_hint_y : None
                height : (len(self.children) / 3) * (Window.height / 3.6)
        
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
                



<BlueCenteredLabel>:
    halign : "center"
    theme_text_color : "Custom"
    text_color : rgba("#2196F3")

"""

from SM import _connection,_session,Base

class BlueCenteredLabel(MDLabel):
    pass


class TableCard(Base):
    
    __tablename__ = "Mesas"

    internalId = Column(Integer,primary_key=True)
    Code = Column(String)
    Closed = Column(Integer)
    InUse = Column(Integer)
    Total = Column(Float)
    Comensales = Column(Integer)
    Childs = Column(Integer)
    Mozo = Column(String)

    def __init__(self,**kwargs):
        super(TableCard,self).__init__(**kwargs)

    def clear_card(self):
        se = _session()
        se.query(TableCard).filter(TableCard.Code == self.Code).\
                            update({TableCard.InUse: 0,
                                    TableCard.Total : 0,
                                    TableCard.Comensales : 0,
                                    TableCard.Childs : 0,
                                    TableCard.Mozo : ""})
        se.commit()
        se.close()
        self.Card.parent.parent.parent.parent.load_tables()

    def load_widget(self):
        self.Card = MDCard(size_hint_y=None,height=Window.height/3.6)
        self.Card.on_release=self.open_table
        self.TableCardGrid = MDGridLayout(cols=2,rows=2,padding=(10,10,10,10),spacing=5)
        self.TableCardGrid.add_widget(BlueCenteredLabel(text="Mesa: %s" % self.Code, font_style="H5"))
        self.TableCardGrid.add_widget(BlueCenteredLabel(text="Mozo: %s" % self.Mozo, font_style="H5"))
        self.TableCardGrid.md_bg_color= [0.333,0.333333,0.333333,0.22222] if self.InUse else [1,1,1,1]
        box = MDBoxLayout(orientation="vertical")
        box.add_widget(BlueCenteredLabel(text="Comensales: %s" % self.Comensales))
        box.add_widget(BlueCenteredLabel(text="Niños: %s" % self.Childs))
        self.TotalLabel = BlueCenteredLabel(text="Total: $%s" % self.Total)
        box.add_widget(self.TotalLabel)
        self.TableCardGrid.add_widget(box)
        self.TableCardGrid.add_widget(Image(source="./images/table.jpg"))
        self.Card.add_widget(self.TableCardGrid)
        return self.Card

    def open_table(self):
        from TableModalView import TableModalView
        view = TableModalView(size=self.Card.parent.size,_card=self, callback=self.save_modal)
        view.open()#,_mesa=self._mesa, _connection=con, callback=self.save_modal)

    def save_modal(self, total):#,modal,total,freetable=False):
        # self.TotalLabel.text = "Total: $%s" % total
        se = _session()
        se.query(TableCard).filter(TableCard.Code == self.Code).\
                            update({TableCard.Total: total,
                                    TableCard.InUse: 1})
        se.commit()
        se.close()
        self.Card.parent.parent.parent.parent.load_tables()

class TablePage(BasePage):
    
    Builder.load_string(tablescreen_kv)

    def __init__(self,**kwargs):
        super(TablePage,self).__init__(**kwargs)
        self.load_tables()

    def load_tables(self, **kwargs):
        self.ids.TableGrid.clear_widgets()

        self.working = True
        
        se = _session()

        for c in se.query(TableCard):
            self.ids.TableGrid.add_widget(c.load_widget())
        
        se.close()
        
        self.working = False
