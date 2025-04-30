from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..controllers import orders as controller
from ..schemas import orders as schema
from ..models import orders as order_model
from ..dependencies.database import engine, get_db


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

    # Check if the promotion code exists
    promotion = db.query(order_model.Promotion).filter(order_model.Promotion.code == promotion_code).first()
    if not promotion or not promotion.check_expiration():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired promotion code")

    # Apply the promotion discount
    if promotion.discount_percentage:
        discount = order.totalPrice * (promotion.discount_percentage / 100)
        order.totalPrice = round(order.totalPrice - discount, 2)

    # Associate the promotion with the order
    order.promotion_code = promotion_code

    # Save the changes
    db.commit()
    db.refresh(order)

    return order
  


@router.put("/{item_id}", response_model=schema.Order)
def update(item_id: int, request: schema.OrderUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)


@router.put("/item_id/{item_id}/status/{status}", response_model=schema.Order)
def update_status(item_id: int, status: str = "Elevate", db: Session = Depends(get_db)):
    if (not (status == "Finished" or status == "Served")):
        status="Elevate"
    return controller.update_status(db=db, item_id=item_id, new_status=status)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)
