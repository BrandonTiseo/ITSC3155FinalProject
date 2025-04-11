from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..controllers import menu as controller
from ..schemas import menu as schema
from ..dependencies.database import get_db

router = APIRouter(
    prefix="/Menu",
    tags=["Menu"],
)

@router.post("/", response_model=schema.MenuItem)
def create_menu_item(menu_item: schema.MenuItemCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, menu_item=menu_item)

@router.get("/", response_model=list[schema.MenuItem])
def read_all_menu_items(db: Session = Depends(get_db)):
    return controller.read_all(db=db)

@router.get("/{menu_item_id}", response_model=schema.MenuItem)
def read_menu_item(menu_item_id: int, db: Session = Depends(get_db)):
    db_menu_item = controller.read_one(db=db, menu_item_id=menu_item_id)
    if db_menu_item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return db_menu_item

@router.put("/{menu_item_id}", response_model=schema.MenuItem)
def update_menu_item(menu_item_id: int, menu_item: schema.MenuItemUpdate, db: Session = Depends(get_db)):
    db_menu_item = controller.update(db=db, menu_item_id=menu_item_id, menu_item=menu_item)
    if db_menu_item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return db_menu_item

@router.delete("/{menu_item_id}", response_model=schema.MenuItem)
def delete_menu_item(menu_item_id: int, db: Session = Depends(get_db)):
    db_menu_item = controller.delete(db=db, menu_item_id=menu_item_id)
    if db_menu_item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return db_menu_item
