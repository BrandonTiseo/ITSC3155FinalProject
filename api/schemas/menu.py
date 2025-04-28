from pydantic import BaseModel
from typing import Optional
from .recipes import Recipe

class MenuItemBase(BaseModel):
    name: str
    price: float
    calories: int
    category: str

class MenuItemCreate(MenuItemBase):
    recipe_items:list[int] = None
    recipe_amounts: list[int] = None

class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    calories: Optional[int] = None
    category: Optional[str] = None

class MenuItem(MenuItemBase):
    id: int
    recipe_items: list[Recipe] = None
    
    class Config:
        from_attributes = True