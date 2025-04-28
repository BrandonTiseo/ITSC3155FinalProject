from sqlalchemy.orm import Session

from datetime import datetime, timezone
from fastapi import HTTPException, status, Response
from ..models import promotion as model
from ..schemas import promotion as schema
from sqlalchemy.exc import SQLAlchemyError

def create(db: Session, promotion: schema.PromotionCreate):
    if db.query(model.Promotion).filter(model.Promotion.code == promotion.code).first() is not None:
        raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail="Promotion with that code already exists!" )
    db_promotion = model.Promotion(**promotion.model_dump())
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


def read_one(db: Session, promotion_code: str):
    db_promotion = db.query(model.Promotion).filter(model.Promotion.code == promotion_code).first()
    if db_promotion and not db_promotion.check_expiration():
        return None  # Expired promotion
    return db_promotion

def update(db: Session, promotion_code, request):
    try:
        db_promotion = db.query(model.Promotion).filter(model.Promotion.code == promotion_code).first()
        if not db_promotion:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion code not found!")
        update_data = request.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_promotion, key, value)


        if db_promotion.expiration and db_promotion.expiration < datetime.now(timezone.utc):
            db_promotion.is_active = False

        db.commit()
        db.refresh(db_promotion)
        return db_promotion
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def delete(db: Session, promotion_code: str):
    promotion = db.query(model.Promotion).filter(model.Promotion.code == promotion_code).first()
    if promotion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion code not found!")
    db.delete(promotion)
    db.commit()
    return promotion