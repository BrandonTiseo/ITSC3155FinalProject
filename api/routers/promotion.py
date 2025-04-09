from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from ..controllers import promotion as controller
from ..schemas import promotion as schema
from ..dependencies.database import get_db

router = APIRouter(
    prefix="/promotions",
    tags=["Promotions"]
)

@router.post("/", response_model=schema.Promotion, status_code=status.HTTP_201_CREATED)
def create_promotion(request: schema.PromotionCreate, db: Session = Depends(get_db)):
    return controller.create(db, request)

@router.get("/", response_model=list[schema.Promotion])
def read_all_promotions(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/{promotion_id}", response_model=schema.Promotion)
def read_one_promotion(promotion_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, promotion_id)

@router.put("/{promotion_id}", response_model=schema.Promotion)
def update_promotion(promotion_id: int, request: schema.PromotionUpdate, db: Session = Depends(get_db)):
    return controller.update(db, promotion_id, request)

@router.delete("/{promotion_id}", response_model=schema.Promotion)
def delete_promotion(promotion_id: int, db: Session = Depends(get_db)):
    return controller.delete(db, promotion_id)