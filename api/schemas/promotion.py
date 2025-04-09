from typing import Optional
from pydantic import BaseModel

class PromotionBase(BaseModel):
    code: str
    discount_percentage: float
    description: Optional[str] = None
    is_active: int = 1 # 1 for active, 0 for inactive

class PromotionCreate(PromotionBase):
    pass

class PromotionUpdate(BaseModel):
    code: Optional[str] = None
    discount_percentage: Optional[float] = None
    description: Optional[str] = None
    is_active: Optional[int] = None

class Promotion(PromotionBase):
    id: int

    class Config:
        orm_mode = True