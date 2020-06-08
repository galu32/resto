from Libs import *
from BaseScreen import *

tablescreen_kv = """     

<TablePage>:

    name : "TablePage"

    MDGridLayout:
        cols : 1

        MDToolbar:
            id : BaseToolbar
            pos_hint : {"top" : 1}
            left_action_items : [['chef-hat', lambda x : None]]
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

<BlueCenteredLabel>:
    halign : "center"
    theme_text_color : "Custom"
    text_color : rgba("#2196F3")

<ListItemWithCheckbox>:
    on_release : self.toogle_check()
    theme_text_color : "Custom"
    text_color : rgba("#2196F3")
    IconLeftWidget:
        icon : root.icon
        theme_text_color : "Custom"
        text_color : rgba("#2196F3")
    RightCheckbox:
        id:check
        theme_text_color : "Custom"
        text_color : rgba("#2196F3")

<ConsumosOneLineListItem>
    on_release : root.remove_item()
    theme_text_color : "Custom"
    text_color : rgba("#2196F3")

<TableModalView>:
    MDCard:
        MDGridLayout:
            cols: 1
    
            MDToolbar:
                id : TableModalViewToolbar
                pos_hint : {"top" : 1}
                left_action_items : [['close', lambda x : root.close_modal()]]
                MDRaisedButton :
                    pos_hint : {"center_x": .5, "center_y": .5}
                    text : "Cobrar Mesa"
                    # on_release: root.load_tables()
                MDRaisedButton :
                    pos_hint : {"center_x": .5, "center_y": .5}
                    text : "Liberar Mesa"
                    on_release : root.close_modal(True)

            MDGridLayout:
                cols : 3
                rows : 1
                MDCard:
                    id: ConsumosCard
                    _total : 0
                    toolbar : ConsumosBottomToolbar
                    orientation : "vertical"
                    MDToolbar:
                        title: "Consumos"
                        pos_hint : {"top" : 1}
                    MDBoxLayout:
                        ScrollView:
                            MDList:
                                id : ConsumosList
                    MDToolbar:
                        id : ConsumosBottomToolbar
                        title : "Total $0"

                MDCard:
                    orientation : "vertical"
                    MDTextField:
                        hint_text : "Buscar articulos..."
                        pos_hint : {"top" : 1}

                    MDBoxLayout:
                        ScrollView:
                            MDList:
                                toolbar : ArticulosToolbar
                                id : ArticulosList

                    ArticulosToolbar:
                        id : ArticulosToolbar
                        title : "Seleccionados: %s" % self._seleccionados
                        right_action_items : [['check', lambda x : self.add_items(ArticulosList, ConsumosList)]]
                
                MDCard:


"""

import mysql.connector
from mysql.connector import errorcode

class SM(ScreenManager):

    _connection = ObjectProperty()

    def __init__(self,**kwargs):
        super(SM,self).__init__(**kwargs)
        
        try:
            self._connection = mysql.connector.connect(user="fran", password="fran", host="localhost", database="resto")
        except:
            pass

class BlueCenteredLabel(MDLabel):
    pass

class ArticulosToolbar(MDToolbar):
    _seleccionados = NumericProperty()
    
    def __init__(self,**kwargs):
        super(ArticulosToolbar,self).__init__(**kwargs)

    def on__seleccionados(self,x,y):
        self.title = "Seleccionados: %s" % self._seleccionados

    def add_items(self,ArticulosList,ConsumosList):
        if not self._seleccionados: return
        self._seleccionados = 0

        for i in ArticulosList.children:
            if i.ids.check.state == "down":
                consumo = ConsumosOneLineListItem(text=i.text)
                ConsumosList.add_widget(consumo)
                consumo._price = i._price
            i.ids.check.state = "normal"

class ConsumosOneLineListItem(OneLineListItem):

    _price = NumericProperty()

    def __init__(self,**kwargs):
        super(ConsumosOneLineListItem,self).__init__(**kwargs)

    def remove_item(self):
        self.parent.parent.parent.parent._total -= self._price
        self.parent.parent.parent.parent.toolbar.title = "Total : $%s" % self.parent.parent.parent.parent._total
        self.parent.remove_widget(self)
    
    def on__price(self,x,y):
        self.parent.parent.parent.parent._total += self._price
        self.parent.parent.parent.parent.toolbar.title = "Total : $%s" % self.parent.parent.parent.parent._total

class ListItemWithCheckbox(OneLineAvatarIconListItem):
    
    icon = StringProperty("food")
    _price = NumericProperty()

    def toogle_check(self):
        toolbar = self.parent.toolbar
        if self.ids.check.state == "normal":
            self.ids.check.state = "down"
            toolbar._seleccionados += 1
        else:
            self.ids.check.state = "normal"
            toolbar._seleccionados -= 1

class RightCheckbox(IRightBodyTouch, MDCheckbox):
    pass

class TableModalView(ModalView):

    _mesa = StringProperty()
    _connection = ObjectProperty()
    working = BooleanProperty(defaultvalue=False)
    callback = ObjectProperty()

    def __init__(self,**kwargs):
        super(TableModalView,self).__init__(**kwargs)
        self.working = True
        self.auto_dismiss = False
        self.size_hint = (None,None)
        self.size = kwargs["size"]
        self.ids.TableModalViewToolbar.title = "Mesa %s" % self._mesa
        t = Thread(target=self.get_items)
        t.start()

    def get_items(self):
        con = self._connection
        if not con: return self.ErrorResponse()
        query = "SELECT * FROM Articulos"
        cursor = con.cursor()
        try:
            cursor.execute(query)
            res = cursor.fetchall()
            for item in res:
                self.ids.ArticulosList.add_widget(
                    ListItemWithCheckbox(text=item[2],_price=item[4])
                )
        except:
            return self.ErrorResponse()
        cursor.close()  
        self.working = False
        self.open()


    def ErrorResponse(self,text=""):
        self.working = False
        if not text: text = "A ocurrido un error vuelve a intentarlo."
        Snackbar(text = text).show()

    def on_working(self,screen,value):
        from BaseScreen import Working
        if value:
            self.add_widget(Working())
        else:
            self.remove_widget(self.children[0])

    def close_modal(self, freetable=False):
        if freetable:
            self.callback(self,self.ids.ConsumosCard._total,freetable)
        else:
            self.callback(self,self.ids.ConsumosCard._total)
        self.dismiss()

class TableCard(MDCard):

    _comensales = NumericProperty()
    _childs = NumericProperty()
    _total = NumericProperty()
    _mozo = StringProperty()
    _mesa = StringProperty()
    _modal = ObjectProperty()
    _in_use = BooleanProperty(defaultvalue=False)

    def __init__(self,**kwargs):
        super(TableCard,self).__init__(**kwargs)
        
        self.size_hint_y = None
        self.height = Window.height / 3.6
        self.on_release = self.open_table

    def load_card(self):
        self.TableCardGrid = MDGridLayout(cols=2,rows=2,padding=(10,10,10,10),spacing=5)
        self.TableCardGrid.add_widget(BlueCenteredLabel(text="Mesa: %s" % self._mesa, font_style="H5"))
        self.TableCardGrid.add_widget(BlueCenteredLabel(text="Mozo: %s" % self._mozo, font_style="H5"))
        box = MDBoxLayout(orientation="vertical")
        box.add_widget(BlueCenteredLabel(text="Comensales: %s" % self._comensales))
        box.add_widget(BlueCenteredLabel(text="Niños: %s" % self._childs))
        self.TotalLabel = BlueCenteredLabel(text="Total: $%s" % self._total)
        box.add_widget(self.TotalLabel)
        self.TableCardGrid.add_widget(box)
        self.TableCardGrid.add_widget(Image(source="./images/table.jpg"))
        self.add_widget(self.TableCardGrid)

    def open_table(self):
        if self._modal:
            return self._modal.open()
        con = self.parent.parent.parent.parent.parent._connection
        view = TableModalView(size=self.parent.size,_mesa=self._mesa, _connection=con, callback=self.save_modal)

    def save_modal(self,modal,total,freetable=False):
        if total:
            if freetable: return self.free_table()
            self._modal = modal
            self._total = total
            self._in_use = True
            self.update_card()
            con = self.parent.parent.parent.parent.parent._connection
            if not con : return Snackbar(text="Error! No hay conexion.").open()
            query = "UPDATE Mesas set InUse = 1, Total = %i WHERE Code = %s" % (self._total,self._mesa)
            cursor = con.cursor()
            try:
                cursor.execute(query)
                con.commit()
            except:
                pass
            cursor.close()

    def free_table(self):
        self._modal = 0
        self._total = 0
        self._in_use = False
        self.update_card()
        con = self.parent.parent.parent.parent.parent._connection
        if not con : return Snackbar(text="Error! No hay conexion.").open()
        query = "UPDATE Mesas set InUse = 0, Total = %i WHERE Code = %s" % (self._total,self._mesa)
        cursor = con.cursor()
        try:
            cursor.execute(query)
            con.commit()
        except:
            pass
        cursor.close()        


    def update_card(self):
        self.TotalLabel.text = "Total: $%s" % self._total

    def on__in_use(self,x,value):
        if value:
            self.TableCardGrid.md_bg_color= [0.333,0.333333,0.333333,0.22222]
        else:
            self.TableCardGrid.md_bg_color= [1,1,1,1]


class TablePage(BasePage):
    
    Builder.load_string(tablescreen_kv)

    def __init__(self,**kwargs):
        super(TablePage,self).__init__(**kwargs)

    def load_tables(self, **kwargs):

        self.working = True

        con = self.parent._connection
        if not con : return self.ErrorResponse()
        query = "SELECT * FROM Mesas"
        cursor = con.cursor()

        try:
            cursor.execute(query)
            res = cursor.fetchall()
        except:
            return self.ErrorResponse()
        cursor.close()

        self.ids.TableGrid.clear_widgets()

        for t in res:
            table = TableCard()
            table._mesa = t[1]
            table._total = t[4]
            table.load_card()
            table._in_use = False if not t[3] else t[3]
            self.ids.TableGrid.add_widget(table)

        self.working = False