from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..controllers import orders as controller
from ..schemas import orders as schema
from ..models import orders as order_model
from ..dependencies.database import engine, get_db
from ..controllers.orders import apply_promotion

router = APIRouter(
    tags=['Orders'],
    prefix="/orders"
)


@router.post("/", response_model=schema.Order)
def create(request: schema.OrderCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Order])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/startYYYY-MM-DDTHH:MM:SS/{startDate}/endYYYY-MM-DDTHH:MM:SS/{endDate}", response_model=list[schema.Order])
def read_by_date(startDate: str, endDate: str, db: Session = Depends(get_db)):
    return controller.read_by_date(db, startDate=startDate, endDate=endDate)


@router.get("/{item_id}", response_model=schema.Order)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)

@router.put("/apply-promotion/{order_id}")
def apply_promotion_to_order(order_id: int, promotion_code: str, db: Session = Depends(get_db)):
    # Get the order to check if it exists
    order = db.query(order_model.Order).filter(order_model.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    # Apply promotion to the order price
    updated_price = apply_promotion(db, order_id, promotion_code, order.totalPrice)

    # Update the order with the new price
    order.totalPrice = updated_price
    db.commit()
    db.refresh(order)

    return {"message": "Promotion applied successfully", "new_total_price": updated_price}

@router.put("/{item_id}", response_model=schema.Order)
def update(item_id: int, request: schema.OrderUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)

@router.put("/item_id/{item_id}/status/{status}", response_model=schema.Order)
def update_status(item_id: int, status: str, db: Session = Depends(get_db)):
    return controller.update_status(db=db, item_id=item_id, new_status=status)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)
