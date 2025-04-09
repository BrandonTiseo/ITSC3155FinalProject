from datetime import datetime
from typing import Optional
from pydantic import BaseModel



class ReviewBase(BaseModel):
    rating: float
    body: Optional[str] = None


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    rating: Optional[float] = None 
    description: Optional[str] = None


class Review(ReviewBase):
    id: int
    
    class ConfigDict:
        from_attributes = True
