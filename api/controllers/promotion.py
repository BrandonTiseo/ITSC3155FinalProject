from sqlalchemy.orm import Session
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
    return db.query(model.Promotion).filter(model.Promotion.id == promotion_id).first()

def update(db: Session, promotion_id: int, promotion: schema.PromotionUpdate):
    db_promotion = db.query(model.Promotion).filter(model.Promotion.id == promotion_id).first()
    if db_promotion is None:
        return None
    for var, value in vars(promotion).items():
        setattr(db_promotion, var, value) if value else None
    db.commit()
    db.refresh(db_promotion)
    return db_promotion


def delete(db: Session, promotion_id: int):
    db_promotion = db.query(model.Promotion).filter(model.Promotion.id == promotion_id).first()
    if db_promotion is None:
        return None
    db.delete(db_promotion)
    db.commit()
    return db_promotion