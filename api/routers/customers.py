from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..controllers import customers as controller
from ..schemas import customer as schema
from ..dependencies.database import get_db

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)

@router.post("/", response_model=schema.Customer)
def create_customer(customer: schema.CustomerCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, customer=customer)

@router.get("/", response_model=list[schema.Customer])
def read_all_customers(db: Session = Depends(get_db)):
    return controller.read_all(db=db)

@router.get("/{name}", response_model=schema.Customer)
def read_customer(name: str, db: Session = Depends(get_db)):
    customer = controller.read_one(db=db, name=name)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.put("/{name}", response_model=schema.Customer)
def update_customer(name: str, update_data: schema.CustomerUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, name=name, update_data=update_data)

@router.delete("/{name}", response_model=schema.Customer)
def delete_customer(name: str, db: Session = Depends(get_db)):
    return controller.delete(db=db, name=name)
