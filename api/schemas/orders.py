from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .order_details import OrderDetail


#basic version of Order, containing only the values we might need to update later
class OrderBase(BaseModel):
    customer_name: str
    description: Optional[str] = None
    status: str
    promotion_code: Optional[str] = None


class OrderCreate(OrderBase):
    order_details:list[int] = None
    item_amounts: list[int] = None


class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


#full version of Order with all information
class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    order_details: list[OrderDetail] = None

    class ConfigDict:
        from_attributes = True
