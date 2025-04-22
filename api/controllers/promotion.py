from sqlalchemy.orm import Session
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
    return db.query(model.Promotion).all()

def read_one(db: Session, promotion_id: int):
    promotion = db.query(model.Promotion).filter(model.Promotion.id == promotion_id).first()
    if promotion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion id not found!")
    return promotion

def update(db: Session, promotion_id, request):
    try:
        promotion = db.query(model.Promotion).filter(model.Promotion.id == promotion_id)
        if not promotion.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion id not found!")
        update_data = request.dict(exclude_unset=True)
        promotion.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return promotion.first()


def delete(db: Session, promotion_id: int):
    promotion = db.query(model.Promotion).filter(model.Promotion.id == promotion_id).first()
    if promotion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion id not found!")
    db.delete(promotion)
    db.commit()
    return promotion