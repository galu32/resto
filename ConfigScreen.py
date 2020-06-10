from Libs import *
from SM import _session
from BaseScreen import *
from SM import UserCard
from TableModalView import ConsumosListItem
from TableScreen import TableCard
from ItemScreen import CategoryCard, ItemCard

Config_kv = """
<ConfigPage>:
    name : "ConfigPage"

    MDGridLayout:
        cols:1
        id : MainGrid
        orientation : "vertical"
        
        MDToolbar:
            id : ItemToolbar
            pos_hint : {"top" : 1}
            left_action_items : [['arrow-left', lambda x : root.go_back()]]

        MDTabs:
            id: android_tabs
            on_tab_switch: root.on_tab_switch(*args)

            Usuarios:
                id : Usuarios
                text : "Usuarios"

            Mesas:
                id : Mesas
                text : "Mesas"

            Categorias:
                text : "Categorias"

            Articulos:
                text : "Articulos"
            
            Recetas:
                text : "Recetas"


<OneLineIconListItem>:
    theme_text_color : "Custom"
    text_color : rgba("#2196F3")

<IconLeftWidget>:
    theme_text_color : "Custom"
    text_color : rgba("#2196F3")

"""

Usuarios_kv = """
<Usuarios>:
    text : "Usuarios"
    MDGridLayout:
        cols : 3
        orientation : "vertical"
        MDCard :
            orientation : "vertical"
            MDToolbar:
                title: "Lista de Usuarios"
                pos_hint : {"top" : 1}
            MDGridLayout:
                cols:1
                spacing : 10
                padding : 10,10,10,10               
                MDCard:
                    ScrollView:
                        MDList:
                            id: UserList

        MDCard :
            MDGridLayout:
                cols:1
                orientation : "vertical"
                
                MDToolbar:
                    title: "Nuevo Usuario"
                    pos_hint : {"top" : 1}

                MDGridLayout:
                    cols:1
                    spacing : 10
                    padding : 10,10,10,10
                    MDCard:
                        MDGridLayout:
                            spacing : 10
                            padding : 10,10,10,10
                            cols:1
                            orientation : "vertical"
                            MDTextField :
                                id : Code
                                hint_text : "Usuario..."
                            MDTextField :
                                hint_text : "Contraseña..."
                                id : Pass
                                password : True
                            MDTextField :
                                id : Name
                                hint_text : "Nombre..."
                            MDBoxLayout:
                                size_hint: .1,None
                                BlueCenteredLabel :
                                    text : "Administrador..."
                                MDCheckbox:
                                    id : Admin

                            MDBoxLayout:
                                size_hint_y : .2
                                pos_hint : {"top": 1}
                                # spacing : 5

                                MDRaisedButton:
                                    text : "Limpiar"
                                    pos_hint : {"center_x": .5, "center_y" : .5}
                                    # size_hint_x : .2
                                    on_release : root.clear_form()

                                MDRaisedButton:
                                    text : "Guardar"
                                    pos_hint : {"center_x": .5, "center_y" : .5}
                                    # size_hint_x : .2
                                    on_release : root.save_user()

        MDCard :
            MDGridLayout:
                cols:1
                rows : 3
                orientation : "vertical"

                MDToolbar:
                    title: "Tipos de Usuarios"
                    pos_hint : {"top" : 1}

                MDGridLayout:
                    cols:1
                    spacing : 10
                    padding : 10,10,10,10
                    MDCard:
                    MDCard:
                        ScrollView:
                            MDList:
                                id: UserTypeList
"""
Mesas_kv = """
<Mesas>:
    MDGridLayout:
        cols : 1   
        MDToolbar:
            title: "Nueva Mesa"
            pos_hint : {"top" : 1}
        MDGridLayout:
            cols : 2

            MDGridLayout:
                cols : 1
                spacing : 10
                size_hint_x : .4
                padding : 10,10,10,10
                orientation : "vertical"
                MDCard:      
                    MDGridLayout:
                        cols : 1
                        padding : 10,10,10,10
                        spacing : 10
                        MDTextField :
                            id : Code
                            hint_text : "Codigo..."
                        MDLabel:

            ScrollView:
                # size_hint_y : None
                # height : root.height

                MDGridLayout:
                    id : TableGrid
                    cols : 3
                    padding : 10,10,10,10
                    spacing : 5
                    size_hint_y : None
                    # height:5000

"""
Categorias_kv = """
<Categorias>:
    MDGridLayout:
        cols : 2

        MDGridLayout:
            cols : 1
            size_hint_x : .4
            MDToolbar:
                title: "Nueva Categoria"
                pos_hint : {"top" : 1}

            MDGridLayout:
                cols:1
                spacing : 10
                padding : 10,10,10,10
                MDCard:
        
        MDGridLayout:
            cols:1
            id : ItemGrid

"""
Articulos_kv = """
<Articulos>:
    MDGridLayout:
        cols : 2

        MDGridLayout:
            cols : 1
            size_hint_x : .4
            MDToolbar:
                title: "Nuevo Articulo"
                pos_hint : {"top" : 1}

            MDGridLayout:
                cols:1
                spacing : 10
                padding : 10,10,10,10
                MDCard:
                    MDGridLayout:
                        spacing : 10
                        padding : 10,10,10,10
                        cols : 1

                        MDTextField:
                            id: Code
                            hint_text: "Codigo..."
                        MDTextField:
                            id: Name
                            hint_text: "Nombre..."
                        MDTextField:
                            id: Price
                            hint_text: "Precio..."
                            input_filter: 'float'

                        MDTextField:
                            id: Category
                            hint_text: "Cateogria..."

                        MDBoxLayout:
                            size_hint_y : .2
                            pos_hint : {"top": 1}
                            # spacing : 5

                            MDRaisedButton:
                                text : "Limpiar"
                                pos_hint : {"center_x": .5, "center_y" : .5}
                                # size_hint_x : .2
                                on_release : root.clear_form()

                            MDRaisedButton:
                                text : "Guardar"
                                pos_hint : {"center_x": .5, "center_y" : .5}
                                # size_hint_x : .2
                                on_release : root.save_item()
        
        MDGridLayout:
            cols:1
            id : ItemGrid
"""

recetas_kv = """
<Recetas>:
    MDGridLayout:
        cols : 3
        MDGridLayout:
            cols : 1
            MDToolbar:
                title: "Recetas disponibles"
            MDGridLayout:
                rows : 2
                cols : 1
                padding:10,10,10,10
                spacing:10
                MDCard:
                    ScrollView:
                        MDList:
                            id: RecipesList
                MDCard:

        MDGridLayout:
            cols : 1
            MDToolbar:
                title: "Nueva Receta"
            MDGridLayout:
                rows : 3
                cols : 1
                padding:10,10,10,10
                # spacing:5
                MDCard:
                    MDGridLayout:
                        spacing : 10
                        padding : 10,10,10,10
                        cols : 1

                        MDTextField:
                            id: Code
                            hint_text: "Codigo..."
                        MDTextField:
                            id: Name
                            hint_text: "Nombre..."
                        MDTextField:
                            id: Price
                            hint_text: "Precio..."
                            input_filter: 'float'

                        MDTextField:
                            id: Category
                            hint_text: "Cateogria..."


                MDCard:
                    orientation : "vertical"
                    BlueCenteredLabel:
                        text : "Articulos disponibles"
                        size_hint_y : .1 
                        font_style : "H5"
                    ScrollView:
                        MDList:
                            id: ItemsList

                MDBoxLayout:
                    size_hint_y : .2
                    pos_hint : {"top": 1}
                    spacing : 5
                    padding:10,10,10,10

                    MDRaisedButton:
                        text : "Limpiar"
                        pos_hint : {"center_x": .5, "center_y" : .5}
                        # size_hint_x : .2
                        on_release : root.clear_form()

                    MDRaisedButton:
                        text : "Guardar"
                        pos_hint : {"center_x": .5, "center_y" : .5}
                        # size_hint_x : .2
                        on_release : root.save_recipe()
        MDGridLayout:
            rows : 2
            cols : 1
            padding:10,10,10,10
            spacing:10
            MDCard:
            MDCard:
"""

class TableConfigCard(TableCard):

    def open_table(self):
        pass

    def load_widget(self):
        self.Card = MDCard(size_hint_y=None,height=Window.height/3.6)
        self.Card.on_release=self.open_table
        self.TableCardGrid = MDGridLayout(cols=2,rows=2,padding=(10,10,10,10),spacing=5)
        self.TableCardGrid.add_widget(BlueCenteredLabel(text="Mesa: %s" % self.Code, font_style="H5"))
        self.TableCardGrid.md_bg_color= [0.333,0.333333,0.333333,0.22222] if self.InUse else [1,1,1,1]
        box = MDBoxLayout(orientation="vertical")
        box2 = MDBoxLayout(orientation="vertical")
        self.TableCardGrid.add_widget(box)
        self.TableCardGrid.add_widget(box2)
        self.TableCardGrid.add_widget(Image(source="./images/table.jpg"))
        self.Card.add_widget(self.TableCardGrid)
        return self.Card

class CategoryConfigCard(CategoryCard):

    def open_category(self):
        pass

class ItemConfigCard(ItemCard):
    pass

class ListItemWithCheckbox(OneLineAvatarIconListItem):
   
    icon = StringProperty("food")
    code = StringProperty()

    def toogle_check(self):
        if self.ids.check.state == "normal":
            self.ids.check.state = "down"
        else:
            self.ids.check.state = "normal"

class Recetas(FloatLayout,MDTabsBase):
    Builder.load_string(recetas_kv)

    def __init__(self,**kwargs):
        super(Recetas,self).__init__(**kwargs)

    def load_content(self):
        self.ids.RecipesList.clear_widgets()
        se = _session()
        for i in se.query(ItemConfigCard):
            if i.Recipe:
                recipe = OneLineIconListItem(
                    text = "%s  -  %s" % (i.Code,i.Name))
                recipe.add_widget(
                    IconLeftWidget(
                        icon = "account-edit",
                        #on_release = self.edit_user
                        ))
                self.ids.RecipesList.add_widget(recipe)
            else:
                item = ListItemWithCheckbox(code=i.Code,text="%s  -  %s" % (i.Code,i.Name))
                self.ids.ItemsList.add_widget(item)
        se.close()

    def clear_form(self):
        self.ids.Code.text = ""
        self.ids.Name.text = ""
        self.ids.Price.text = ""
        self.ids.Category.text = ""
        for c in self.ids.ItemsList.children:
            c.ids.check.state = "normal"

    def save_recipe(self):
        if not self.ids.Code.text or not self.ids.Name.text or not self.ids.Price.text or not self.ids.Category.text:
            return Snackbar(text="Se debe completar todos los campos.").show()
        rec = ""
        for r in self.ids.ItemsList.children:
            if r.ids.check.state == "down":
                rec += r.code + ","
                r.ids.check.state == "normal"
        if not rec: return Snackbar(text="No se selecciono ningun articulo para incluir en la recepta.").show()
        se = _session()
        item = ItemConfigCard()
        item.Code = self.ids.Code.text
        item.Name = self.ids.Name.text
        item.Price = self.ids.Price.text
        item.Category = self.ids.Category.text
        item.Recipe = 1
        item.RecipeContent = rec[:-1]
        try :
            se.add(item)
            se.commit()
        except exc.IntegrityError:
            se.close()
            return Snackbar(text="El codigo de articulo ya existe.").show()
        se.close()
        self.load_content()
        self.clear_form()

class Articulos(FloatLayout,MDTabsBase):

    Builder.load_string(Articulos_kv)

    def __init__(self,**kwargs):
        super(Articulos,self).__init__(**kwargs)

    def load_content(self):
        se = _session()
        res = se.query(ItemConfigCard)
        if res.count():
            self.ids.ItemGrid.clear_widgets()
            grid = MDGridLayout(
                cols = 2, padding=(10,10,10,10), spacing=10)

            for i in res:
                c = i.load_widget()
                i.on_release = self.edit_item
                grid.add_widget(c)

            self.ids.ItemGrid.add_widget(grid)

    def edit_item(self,item):
        self.ids.Code.text = item.Code
        self.ids.Name.text = item.Name
        # self.ids.Price.text = float(item.Price)
        self.ids.Category.text = item.Category

    def clear_form(self):
        self.ids.Code.text = ""
        self.ids.Name.text = ""
        self.ids.Price.text = ""
        self.ids.Category.text = ""

    def save_item(self):
        if not self.ids.Code.text or not self.ids.Name.text or not self.ids.Price.text or not self.ids.Category.text:
            return Snackbar(text="Se debe completar todos los campos.").show()
        se = _session()
        item = ItemConfigCard()
        item.Code = self.ids.Code.text
        item.Name = self.ids.Name.text
        item.Price = self.ids.Price.text
        item.Category = self.ids.Category.text
        item.Recipe = 0
        item.RecipeContent = None

        try :
            se.add(item)
            se.commit()
        except exc.IntegrityError:
            se.close()
            return Snackbar(text="El codigo de articulo ya existe.").show()
        se.close()
        self.clear_form()
        self.load_content()

class Categorias(FloatLayout,MDTabsBase):

    Builder.load_string(Categorias_kv)

    def __init__(self,**kwargs):
        super(Categorias,self).__init__(**kwargs)

    def load_content(self):
        se = _session()
        res = se.query(CategoryConfigCard)
        if res.count():
            self.ids.ItemGrid.clear_widgets()
            grid = MDGridLayout(
                    cols = 2, padding=(10,10,10,10), spacing=10)
            for c in res:
                card = c.load_widget()
                grid.add_widget(card)
            self.ids.ItemGrid.add_widget(grid)
        se.close()

class Mesas(FloatLayout, MDTabsBase):

    Builder.load_string(Mesas_kv)

    def __init__(self,**kwargs):
        super(Mesas,self).__init__(**kwargs)

    def load_content(self):
        self.ids.TableGrid.clear_widgets()  
        se = _session()
        for c in se.query(TableConfigCard):
            self.ids.TableGrid.add_widget(c.load_widget())
        # self.ids.TableGrid.height = len(self.ids.TableGrid.children) / 3 * (Window.height / 3.6) + (len(self.ids.TableGrid.children) *10)
        se.close()

class Usuarios(FloatLayout, MDTabsBase):

    Builder.load_string(Usuarios_kv)

    def __init__(self,**kwargs):
        super(Usuarios,self).__init__(**kwargs)

    def load_content(self):
        self.ids.UserList.clear_widgets()
        self.ids.UserTypeList.clear_widgets()
        se = _session()
        for user in se.query(UserCard):
            item = OneLineIconListItem(
                text = "Usuario : %s" % user.Code)
            item.add_widget(
                IconLeftWidget(
                    icon = "account-edit",
                    on_release = self.edit_user))


            # self.ids.UserTypeList.add_widget(typebox)
            self.ids.UserList.add_widget(item)
        se.close()

    def clear_form(self):
        self.ids.Code.text = ""
        self.ids.Pass.text = ""
        self.ids.Name.text = ""
        self.ids.Admin.state = "normal"

    def save_user(self):
        if not self.ids.Code.text or not self.ids.Pass.text or not self.ids.Name.text:
            return Snackbar(text="Se debe completar todos los campos.").show()
        se = _session()
        user = UserCard()
        user.Code = self.ids.Code.text
        user.Pass = self.ids.Pass.text
        user.Name = self.ids.Name.text
        user.Type = 0
        user.Admin = 1 if self.ids.Admin.state == "down" else 0
        try :
            se.add(user)
            se.commit()
        except exc.IntegrityError:
            se.close()
            return Snackbar(text="El codigo de usuario ya existe.").show()
        se.close()
        self.load_content() 
        self.clear_form()

    def edit_user(self,x):
        text = x.parent.parent.text
        formated_text = text.replace(" ", "").split(":")
        se = _session()
        q = se.query(UserCard).filter(UserCard.Code == formated_text[1])
        se.close()
        if not q.count(): return Snackbar(text="A ocurrido un error.").show()
        content = MDGridLayout(cols=1, spacing=5,padding=(10,10,10,10),md_bg_color=[1,1,1,1])        
        text1 = MDTextField(text=q[0].Code)
        text1.hint_text = "Usuario..."
        text2 = MDTextField(password=True,text=q[0].Pass)
        text2.hint_text = "Contraseña..."
        text3 = MDTextField(text=q[0].Name)
        text3.hint_text = "Nombre..."

        b1 = MDRaisedButton(
                    text="Cancelar", on_release=lambda x: self.update_user(False),
                    pos_hint = {"center_x": .5, "center_y": .5}
                )
        b2 = MDRaisedButton(
                    text="Aceptar", on_release=lambda x: self.update_user(True,{
                        "Code" : text1,
                        "Pass" : text2,
                        "Name" : text3
                        }),
                    pos_hint = {"center_x": .5, "center_y": .5}
                )

        b3 = MDRaisedButton(
                    text="Eliminar Usuario", on_release=lambda x: self.delete_user(text1.text),
                    pos_hint = {"center_x": .5, "center_y": .5}
                )

        bbox = MDGridLayout(cols=2,spacing=30,padding=(10,10,10,0))
        bbox.add_widget(b1)
        bbox.add_widget(b2)
        # content.add_widget(text1)
        content.add_widget(text2)
        content.add_widget(text3)
        content.add_widget(bbox)
        content.add_widget(b3)
        self.vw = ModalView(auto_dismiss=False,size = content.size, size_hint=(.3,.3))
        self.vw.add_widget(content)
        self.vw.open()


    def update_user(self,value,fields=None):
        if value:
            for field in fields:
                if not fields[field].text: return Snackbar(text="Se deben completar todos los campos.").show()
            se = _session()
            se.query(UserCard).filter(UserCard.Code == fields["Code"].text).update({
                UserCard.Pass : fields["Pass"].text,
                UserCard.Name : fields["Name"].text
                })
            se.commit()
            se.close()
            self.load_content()
        self.vw.dismiss()

    def delete_user(self,code):
        se = _session()
        q = se.query(UserCard).filter(UserCard.Code == code)
        if q.count():
            q.delete()
            se.commit()
        se.close()
        self.vw.dismiss()
        self.load_content()

class ConfigPage(BasePage):

    Builder.load_string(Config_kv)
    
    def go_back(self):
        self.parent.current = "TablePage"

    def load_users(self):
        self.ids.Usuarios.load_content()

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        instance_tab.load_content()