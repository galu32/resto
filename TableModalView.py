from Libs import *
from SM import _session, Base

tablemodalview_kv = """

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

<ConsumosListItem>
    theme_text_color : "Custom"
    text_color : rgba("#2196F3")

<TableModalView>:
    MDCard:
        MDGridLayout:
            cols: 1
    
            MDToolbar:
                id : TableModalViewToolbar
                pos_hint : {"top" : 1}
                title : "Mesa %s" % root._card.Code
                left_action_items : [['check', lambda x : root.close_modal()]]
                
                MDRaisedButton :
                    pos_hint : {"center_x": .5, "center_y": .5}
                    text : "Cobrar Mesa"
                    # on_release: root.load_tables()
                
                MDRaisedButton :
                    pos_hint : {"center_x": .5, "center_y": .5}
                    text : "Liberar Mesa"
                    on_release : root.free_table()

            MDGridLayout:
                cols : 3
                rows : 1

                MDCard:
                    id: ConsumosCard
                    toolbar : ConsumosBottomToolbar
                    orientation : "vertical"
                    MDToolbar:
                        title: "Consumos"
                        pos_hint : {"top" : 1}
                    MDBoxLayout:
                        ScrollView:
                            MDList:
                                _total:0
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
                        right_action_items : [['check', lambda x : root.add_items()]]
                
                MDCard:
"""

class ConsumosListItem(OneLineListItem):
    pass

class RightCheckbox(IRightBodyTouch, MDCheckbox):
    pass

class TableModalView(ModalView):
    
    Builder.load_string(tablemodalview_kv)
    _card = ObjectProperty()
    working = BooleanProperty(defaultvalue=False)
    callback = ObjectProperty()

    def __init__(self,**kwargs):
        super(TableModalView,self).__init__(**kwargs)
        self.working = True
        self.auto_dismiss = False
        self.size_hint = (None,None)
        # self.size = kwargs["size"]
        self.get_items()

    def get_items(self):
        from ItemScreen import ItemCard
        se = _session()

        for item in se.query(ItemCard):
            self.ids.ArticulosList.add_widget(
                ListItemWithCheckbox(text=item.Name,_price=item.Price)
                )

        consumos = se.query(ConsumosOneLineListItem).filter(ConsumosOneLineListItem.Code == self._card.Code)
        for cons in consumos:
            self.ids.ConsumosList._total += cons.Price
            widget = cons.load_widget()
            self.ids.ConsumosList.add_widget(widget)

        if self.ids.ConsumosList._total:
            self.ids.ConsumosBottomToolbar.title = "Total $%s" % self.ids.ConsumosList._total
        se.close()
        self.working = False


    def on_working(self,screen,value):
        from BaseScreen import Working
        if value:
            self.add_widget(Working())
        else:
            self.remove_widget(self.children[0])

    def add_items(self):
        if not self.ids.ArticulosToolbar._seleccionados: return
        self.ids.ArticulosToolbar._seleccionados = 0
        se = _session()
        for i in self.ids.ArticulosList.children:
            if i.ids.check.state == "down":
                consumo = ConsumosOneLineListItem(Code=self._card.Code, Name=i.text, Price=i._price)
                self.ids.ConsumosList._total += i._price
                se.add(consumo)
                widget = consumo.load_widget()
                self.ids.ConsumosList.add_widget(widget)
            i.ids.check.state = "normal"
        self.ids.ConsumosBottomToolbar.title = "Total $%s" % self.ids.ConsumosList._total
        se.commit()
        se.close()

    def close_modal(self):
        self.callback(self.ids.ConsumosList._total)
        self.dismiss()

    def free_table(self):
        self.AskYesNo = MDDialog(
            auto_dismiss=False,
            # title="[color=f54242]La venta de este pack se realiza de forma anonima, por lo que enviaremos un mail para que el vendedor se ponga en contacto![/color]",
            text="Esta seguro? Se eliminaran todos los consumos y se liberara la mesa.",
            type="custom",
            # content_cls = content,
            buttons=[
                MDRaisedButton(
                    text="Cancelar", on_release=lambda x: self.free_table_ask(False)
                ),
                MDRaisedButton(
                    text="Aceptar", on_release=lambda x: self.free_table_ask(True)
                ),

            ],
        )
        self.AskYesNo.open()

    def free_table_ask(self,value):
        if not value: return self.AskYesNo.dismiss()
        self.clear_consumos()
        self._card.clear_card()
        self.dismiss()
        self.AskYesNo.dismiss()

    def clear_consumos(self):
        self.ids.ConsumosList.clear_widgets()
        se = _session()
        se.query(ConsumosOneLineListItem).filter(ConsumosOneLineListItem.Code==self._card.Code).delete()
        se.commit()
        se.close()

class ArticulosToolbar(MDToolbar):

    _seleccionados = NumericProperty()
    
    def __init__(self,**kwargs):
        super(ArticulosToolbar,self).__init__(**kwargs)

    def on__seleccionados(self,x,y):
        self.title = "Seleccionados: %s" % self._seleccionados


class ConsumosOneLineListItem(Base):

    __tablename__ = "Consumos"

    internalId = Column(Integer,primary_key=True)
    Code = Column(String)
    Price = Column(Float)
    Name = Column(String)

    def __init__(self,**kwargs):
        super(ConsumosOneLineListItem,self).__init__(**kwargs)

    def load_widget(self):
        item = ConsumosListItem(text=self.Name)
        item.on_release = lambda : self.remove_item(item)
        return item

    def remove_item(self,item):
        se = _session()
        se.query(ConsumosOneLineListItem).filter(ConsumosOneLineListItem.internalId==self.internalId).delete()
        se.commit()
        se.close()
        item.parent._total -= self.Price
        item.parent.parent.parent.parent.toolbar.title = "Total $%s" % item.parent._total
        item.parent.remove_widget(item)

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