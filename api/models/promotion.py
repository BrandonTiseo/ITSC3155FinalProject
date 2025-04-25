from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from ..dependencies.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class Promotion(Base):
    __tablename__ = "promotions"

    code = Column(String(100), primary_key=True, index=True)
    discount_percentage = Column(Float, nullable=False)
    description = Column(String(255), nullable=True)
    is_active = Column(Boolean)
    expiration = Column(DateTime(timezone=True), nullable=False)  # expiration date 
    orders = relationship("Order", back_populates="promotion")


    # Automatically check if promotion is expired when querying the promotion
    def check_expiration(self):
        if self.expiration and self.expiration < datetime.utcnow():
            self.is_active = false
            return False
        return True
