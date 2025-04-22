from pydantic import BaseModel
from typing import Optional

class CustomerBase(BaseModel):
    name: str
    email: str
    phone_number: str
    address: str
    card_num: str
    card_type: str

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    card_num: Optional[str] = None
    card_type: Optional[str] = None

class Customer(CustomerBase):
    class Config:
        orm_mode = True
