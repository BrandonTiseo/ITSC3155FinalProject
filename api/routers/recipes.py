from fastapi import APIRouter, Depends, FastAPI, status, Response
from sqlalchemy.orm import Session
from ..controllers import recipes as controller
from ..schemas import recipes as schema
from ..dependencies.database import engine, get_db

router = APIRouter(
    tags=['Recipes'],
    prefix="/recipes"
)


# @router.post("/", response_model=schema.OrderDetail)
# def create(request: schema.OrderDetailCreate, db: Session = Depends(get_db)):
#     return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Recipe])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{recipe_id}", response_model=schema.Recipe)
def read_one(recipe_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, recipe_id=recipe_id)


# @router.put("/{item_id}", response_model=schema.OrderDetail)
# def update(item_id: int, request: schema.OrderDetailUpdate, db: Session = Depends(get_db)):
#     return controller.update(db=db, request=request, item_id=item_id)


# @router.delete("/{item_id}")
# def delete(item_id: int, db: Session = Depends(get_db)):
#     return controller.delete(db=db, item_id=item_id)
