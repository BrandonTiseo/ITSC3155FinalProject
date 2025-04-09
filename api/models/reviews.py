from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Review(Base):
    __tablename__ = "Reviews"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    rating = Column(DECIMAL(2,1), nullable = False, server_default='0.0')
    body = Column(String(500))
