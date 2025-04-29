import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

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

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_name = Column(String(100)) 
    promotion_code = Column(String(100), ForeignKey("promotions.code")) 
    order_date = Column(DateTime, nullable=False, server_default=str(datetime.now()))
    description = Column(String(300))
    status = Column(String(50))
    type = Column(String(50))
    totalPrice = Column(Float(2))


    order_details = relationship("OrderDetail", back_populates="order", uselist=True, cascade='all,delete')
    promotion= relationship("Promotion", back_populates="orders")


"""
Old Version for reference:

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_name = Column(String(100))
    order_date = Column(DATETIME, nullable=False, server_default=str(datetime.now()))
    description = Column(String(300))

    order_details = relationship("OrderDetail", back_populates="order")
"""