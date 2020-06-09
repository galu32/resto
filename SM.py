from Libs import *
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker


_connection = create_engine('mysql+pymysql://fran:fran@localhost/resto',echo=True)
_session = sessionmaker(bind=_connection, expire_on_commit=False)
Base = declarative_base(_connection)

class SM(ScreenManager):

    _current_user = ObjectProperty()

    def __init__(self,**kwargs):
        super(SM,self).__init__(**kwargs)

    def login_dialog(self):
            content = MDGridLayout(cols=1, spacing=5,padding=(10,10,10,10),md_bg_color=[1,1,1,1])
            
            text1 = MDTextField()
            text1.hint_text = "Usuario..."
            text2 = MDTextField(password=True)
            text2.hint_text = "Contraseña..."

            b1 = MDRaisedButton(
                        text="Cancelar", on_release=lambda x: self.login(False),
                        pos_hint = {"center_x": .5, "center_y": .5}
                    )
            b2 = MDRaisedButton(
                        text="Aceptar", on_release=lambda x: self.login(True,{
                            "Code" : text1,
                            "Pass" : text2,
                            }),
                        pos_hint = {"center_x": .5, "center_y": .5}
                    )
            bbox = MDGridLayout(cols=2,spacing=30,padding=(10,10,10,0))
            bbox.add_widget(b1)
            bbox.add_widget(b2)
            content.add_widget(text1)
            content.add_widget(text2)
            content.add_widget(bbox)
            self.vw = ModalView(auto_dismiss=False,size = content.size, size_hint=(.3,.25))
            self.vw.add_widget(content)
            self.vw.open()

    def login(self,value,fields=None):
        if value:
            for field in fields:
                if not fields[field].text:
                    return Snackbar(text="Se deben completar todos los campos.").show()
            se = _session()
            q = se.query(UserCard).filter(UserCard.Code == fields["Code"].text, UserCard.Pass == fields["Pass"].text)
            if not q.count():
                return Snackbar(text="Usuario o contraseña incorrecta").show()
            self._current_user = q[0]
            ## provisorio
            self.children[0].ids.nav_drawer._current_user = q[0]
            ## provisorio
        self.vw.dismiss()

class UserCard(Base):

    __tablename__ = "Usuarios"
    internalId = Column(Integer, primary_key=True)
    Code = Column(String)
    Pass = Column(String)
    Name = Column(String)
    Admin = Column(Integer)

