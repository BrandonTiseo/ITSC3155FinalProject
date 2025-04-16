from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models.customer import Customer
from ..schemas.customer import CustomerCreate, CustomerUpdate

def create(db: Session, customer: CustomerCreate):
    db_customer = Customer(**customer.dict())
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


def update(db: Session, name: str, update_data: CustomerUpdate):
    customer = db.query(Customer).filter(Customer.name == name).first()
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer name not found!")
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(customer, key, value)
    db.commit()
    db.refresh(customer)
    return customer

def delete(db: Session, name: str):
    customer = db.query(Customer).filter(Customer.name == name).first()
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer name not found!")
    db.delete(customer)
    db.commit()
    return customer
