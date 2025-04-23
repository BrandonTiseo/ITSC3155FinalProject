from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .resources import Resource



class RecipeBase(BaseModel):
    amount: int


class RecipeCreate(RecipeBase):
    menu_item_id: int
    resource_id: int

class RecipeUpdate(BaseModel):
    menu_item_id: Optional[int] = None
    resource_id: Optional[int] = None
    amount: Optional[int] = None

class Recipe(RecipeBase):
    id: int
    menu_item_id: int 
    resource: Resource

    class ConfigDict:
        from_attributes = True