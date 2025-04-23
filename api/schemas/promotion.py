from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class PromotionBase(BaseModel):
    code: str
    discount_percentage: float
    description: Optional[str] = None
    is_active: bool
    expiration: datetime


class PromotionCreate(PromotionBase):
    pass

class PromotionUpdate(BaseModel):
    code: Optional[str] = None
    discount_percentage: Optional[float] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    expiration: Optional[datetime] = None

class Promotion(PromotionBase):
    code: str

    class Config:
        orm_mode = True