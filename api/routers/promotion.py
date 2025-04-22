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

@router.get("/{promotion_code}", response_model=schema.Promotion)
def read_one_promotion(promotion_code: str, db: Session = Depends(get_db)):
    return controller.read_one(db=db, promotion_code=promotion_code)

@router.put("/{promotion_code}", response_model=schema.Promotion)
def update_promotion(promotion_code: str, request: schema.PromotionUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, promotion_code=promotion_code, request=request)

@router.delete("/{promotion_code}", response_model=schema.Promotion)
def delete_promotion(promotion_code: str, db: Session = Depends(get_db)):
    return controller.delete(db, promotion_code)