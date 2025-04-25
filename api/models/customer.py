from sqlalchemy import Column, String, Integer, Boolean
from ..dependencies.database import Base

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index = True, autoincrement=True)
    name = Column(String(100))
    email = Column(String(100), nullable=False)
    phone_number = Column(String(15), nullable=False)
    address = Column(String(255), nullable=False)
    card_num = Column(String(20), nullable=False)
    card_type = Column(String(50), nullable=False)
    is_guest = Column(Boolean, default=False)
