from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class MenuItem(Base):
    __tablename__ = "menu_items"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    ingredients = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    calories = Column(Integer, nullable=False)
    category = Column(String(50), nullable=False) 
    
    order_details = relationship("OrderDetail", back_populates="menu_item")
