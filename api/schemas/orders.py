from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .order_details import OrderDetail


"""
Order Statuses:
Received
Finished
Served
"""

"""
Order types:
DineIn
Takeout
Delivery
"""

#basic version of Order, containing only the values we initialize right off the bat
class OrderBase(BaseModel):

    customer_name: str
    description: Optional[str] = None
    status: str
    customer_name: str = "Scoobert G. Boinkus"
    description: Optional[str] = "No customer modifications"
    status: Optional[str] = "Received"
    type: Optional[str] = "Takeout"

    

#data we need to create an order, that isn't in base
class OrderCreate(OrderBase):
    order_details:list[int] = None
    item_amounts: list[int] = None

#fields we might want to update later
class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None
    promotion_code: Optional[str] = None
    totalPrice: Optional[float] = None


#full version of Order with all information
class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    order_details: list[OrderDetail] = None
    totalPrice: Optional[float] = None

    class ConfigDict:
        from_attributes = True
