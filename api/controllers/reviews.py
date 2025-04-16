from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import reviews as model
from sqlalchemy.exc import SQLAlchemyError

def create(db: Session, request):
    new_item = model.Review(
        rating = request.rating,
        body = request.body
    )
    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
    return new_item


def read_all(db: Session):
    try:
        reviews = db.query(model.Review).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return reviews


def read_one(db: Session, item_id):
    try:
        review = db.query(model.Review).filter(model.Review.id == item_id).first()
        if review is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return review


def update(db: Session, item_id, request):
    try:
        review = db.query(model.Review).filter(model.Review.id == item_id)
        if not review.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review id not found!")
        update_data = request.dict(exclude_unset=True)
        review.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return review.first()


def delete(db: Session, item_id):
    try:
        review = db.query(model.Review).filter(model.Review.id == item_id)
        if not review.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review id not found!")
        review.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


