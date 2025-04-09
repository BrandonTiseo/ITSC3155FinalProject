from pydantic import BaseModel
from typing import Optional

class MenuItemBase(BaseModel):
    name: str
    ingredients: str
    price: float
    calories: int
    category: str

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    ingredients: Optional[str] = None
    price: Optional[float] = None
    calories: Optional[int] = None
    category: Optional[str] = None

class MenuItem(MenuItemBase):
    id: int

    class Config:
        orm_mode = True
