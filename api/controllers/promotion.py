from sqlalchemy.orm import Session
from datetime import datetime, timezone
from ..models import promotion as model
from ..schemas import promotion as schema

def create(db: Session, promotion: schema.PromotionCreate):
    db_promotion = model.Promotion(**promotion.dict())
    if db_promotion.expiration and db_promotion.expiration < datetime.now(timezone.utc):
        db_promotion.is_active = 0
    db.add(db_promotion)
    db.commit()
    db.refresh(db_promotion)
    return db_promotion

def read_all(db: Session):
    promotions = db.query(model.Promotion).all()
     # Check if promotions are expired and update is_active
    for promotion in promotions:
        promotion.check_expiration()
    return promotions


def read_one(db: Session, promotion_id: int):
    db_promotion = db.query(model.Promotion).filter(model.Promotion.id == promotion_id).first()
    if db_promotion and not db_promotion.check_expiration():
        return None  # Expired promotion
    return db_promotion

def update(db: Session, promotion_id: int, promotion: schema.PromotionUpdate):
    db_promotion = db.query(model.Promotion).filter(model.Promotion.id == promotion_id).first()
    if db_promotion is None:
        return None
    for var, value in vars(promotion).items():
        setattr(db_promotion, var, value) if value else None
    # Check expiration and update is_active if necessary
    if db_promotion.expiration and db_promotion.expiration < datetime.now(timezone.utc):
        db_promotion.is_active = 0
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