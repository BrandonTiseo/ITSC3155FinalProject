from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas import resources as schema
from ..controllers import resources as controller
from ..dependencies.database import get_db

router = APIRouter(
    prefix="/resources",
    tags=["Resources"]
)


@router.post("/", response_model=schema.Resource)
def create(request: schema.ResourceCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Resource])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{resource_id}", response_model=schema.Resource)
def read_one(resource_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, resource_id=resource_id)


@router.put("/{resource_id}", response_model=schema.Resource)
def update(resource_id: int, request: schema.ResourceUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, resource_id=resource_id)


@router.delete("/{resource_id}")
def delete(resource_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, resource_id=resource_id)