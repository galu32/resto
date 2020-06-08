from Libs import *
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker


_connection = create_engine('mysql+pymysql://fran:fran@localhost/resto',echo=True)
_session = sessionmaker(bind=_connection, expire_on_commit=False)
Base = declarative_base(_connection)

class SM(ScreenManager):

    def __init__(self,**kwargs):
        super(SM,self).__init__(**kwargs)