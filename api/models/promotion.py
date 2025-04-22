from sqlalchemy import Column, Integer, String, Float, Boolean
from ..dependencies.database import Base

class Promotion(Base):
    __tablename__ = "promotions"
    code = Column(String(100), primary_key=True, index=True)
    discount_percentage = Column(Float, nullable=False)
    description = Column(String(255), nullable=True)
    is_active = Column(Boolean)