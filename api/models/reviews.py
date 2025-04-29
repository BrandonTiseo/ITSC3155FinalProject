from sqlalchemy import Column, Integer, String, DECIMAL
from ..dependencies.database import Base


class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    rating = Column(DECIMAL(2,1), nullable = False, server_default='0.0')
    body = Column(String(500))
