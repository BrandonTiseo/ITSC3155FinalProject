from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import promotion as model
from ..schemas import promotion as schema

def create(db: Session, promotion: schema.PromotionCreate):
    db_promotion = model.Promotion(**promotion.dict())
    db.add(db_promotion)
    db.commit()
    db.refresh(db_promotion)
    return db_promotion

def read_all(db: Session):
    return db.query(model.Promotion).all()

def read_one(db: Session, promotion_id: int):
    promotion = db.query(model.Promotion).filter(model.Promotion.id == promotion_id).first()
    if promotion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion id not found!")
    return promotion

def update(db: Session, promotion_id: int, promotion: schema.PromotionUpdate):
    promotion = db.query(model.Promotion).filter(model.Promotion.id == promotion_id).first()
    if promotion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion id not found!")
    for var, value in vars(promotion).items():
        setattr(promotion, var, value) if value else None
    db.commit()
    db.refresh(promotion)
    return promotion


def delete(db: Session, promotion_id: int):
    promotion = db.query(model.Promotion).filter(model.Promotion.id == promotion_id).first()
    if promotion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion id not found!")
    db.delete(promotion)
    db.commit()
    return promotion