from Libs import *
from SM import Base

class ItemsPage(Base):
    
    __tablename__ = "Articulos"

    internalId = Column(Integer,primary_key=True)
    Code = Column(String)
    Name = Column(String)
    Closed = Column(Integer)
    Price = Column(Float)