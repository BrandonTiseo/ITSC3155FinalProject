from sqlalchemy import Column, Integer, String, Float
from ..dependencies.database import Base

class Promotion(Base):
    __tablename__ = "promotions"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(100), nullable=False, unique=True)
    discount_percentage = Column(Float, nullable=False)
    description = Column(String(255), nullable=True)
    is_active = Column(Integer, nullable=False, default=0)  # 1 for active, 0 for inactive