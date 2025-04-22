from sqlalchemy import Column, Integer, String, Float, DateTime
from ..dependencies.database import Base
from datetime import datetime

class Promotion(Base):
    __tablename__ = "promotions"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(100), nullable=False, unique=True)
    discount_percentage = Column(Float, nullable=False)
    description = Column(String(255), nullable=True)
    is_active = Column(Integer, nullable=False, default=1)  # 1 for active, 0 for inactive
    expiration = Column(DateTime(timezone=True), nullable=False)  # expiration date 


    # Automatically check if promotion is expired when querying the promotion
    def check_expiration(self):
        if self.expiration and self.expiration < datetime.utcnow():
            self.is_active = 0
            return False
        return True