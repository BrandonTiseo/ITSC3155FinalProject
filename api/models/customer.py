from sqlalchemy import Column, String, Integer
from ..dependencies.database import Base

class Customer(Base):
    __tablename__ = "customers"

    name = Column(String(100), primary_key=True, index=True)
    email = Column(String(100), nullable=False)
    phone_number = Column(String(15), nullable=False)
    address = Column(String(255), nullable=False)
    card_num = Column(String(20), nullable=False)
    card_type = Column(String(50), nullable=False)
