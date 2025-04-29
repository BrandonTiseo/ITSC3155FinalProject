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


@router.get("/{id}", response_model=schema.Customer)
def read_customer(id: int, db: Session = Depends(get_db)):
    customer = controller.read_one(db=db, id=id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.put("/{id}", response_model=schema.Customer)
def update_customer(id: int, update_data: schema.CustomerUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, id=id, request=update_data)


@router.delete("/{id}", response_model=schema.Customer)
def delete_customer(id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, id=id)


@router.post("/guests/")
def create_guest(guest: schema.GuestCreate, db: Session = Depends(get_db)):
    return controller.create_guest(db=db, guest=guest)


@router.delete("/guests/")
def delete_guests(db: Session = Depends(get_db)):
    return controller.delete_all_guests(db=db)