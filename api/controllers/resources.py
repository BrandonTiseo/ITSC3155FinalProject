from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import resources as model
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):
    new_resource = model.Resource(
        name=request.name,
        amount=request.amount,
        unit=request.unit,

    )

    try:
        db.add(new_resource)
        db.commit()
        db.refresh(new_resource)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_resource


def read_all(db: Session):
    try:
        result = db.query(model.Resource).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, resource_id):
    try:
        resource = db.query(model.Resource).filter(model.Resource.id == resource_id).first()
        if resource is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return resource


def update(db: Session, resource_id, request):
    try:
        resource = db.query(model.Resource).filter(model.Resource.id == resource_id)
        if not resource.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource id not found!")
        update_data = request.dict(exclude_unset=True)
        resource.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return resource.first()


def delete(db: Session, resource_id):
    try:
        resource = db.query(model.Resource).filter(model.Resource.id == resource_id)
        if not resource.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource id not found!")
        resource.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)