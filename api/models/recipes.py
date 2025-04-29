from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base
from sqlalchemy import UniqueConstraint


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"))
    resource_id = Column(Integer, ForeignKey("resources.id"))
    amount = Column(Integer, index=True, nullable=False, server_default='0.0')

    menu_item = relationship("MenuItem", back_populates="recipe_items")
    resource = relationship("Resource", back_populates="recipes")
    
    __table_args__ = (
    UniqueConstraint('menu_item_id', 'resource_id', name='uix_menu_resource'),
    )