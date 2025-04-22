from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models.customer import Customer
from ..schemas.customer import CustomerCreate
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, customer: CustomerCreate):
    if db.query(Customer).filter(Customer.name == customer.name).first() is not None:
        raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail="Customer with that name already exists!" )
    db_customer = Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def read_all(db: Session):
    return db.query(Customer).all()

def read_one(db: Session, name: str):
    customer = db.query(Customer).filter(Customer.name == name).first()
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer name not found!")
    return customer


def update(db: Session, name, request):
    try:
        customer = db.query(Customer).filter(Customer.name == name)
        if not customer.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer name not found!")
        update_data = request.dict(exclude_unset=True)
        customer.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return customer.first()

def delete(db: Session, name: str):
    customer = db.query(Customer).filter(Customer.name == name).first()
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer name not found!")
    db.delete(customer)
    db.commit()
    return customer
