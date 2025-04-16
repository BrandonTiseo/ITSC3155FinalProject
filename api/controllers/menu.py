from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import menu as model
from ..schemas import menu as schema

def create(db: Session, menu_item: schema.MenuItemCreate):
    db_menu_item = model.MenuItem(**menu_item.dict())
    db.add(db_menu_item)
    db.commit()
    db.refresh(db_menu_item)
    return db_menu_item

def read_all(db: Session):
    return db.query(model.MenuItem).all()

def read_one(db: Session, menu_item_id: int):
    menu_item = db.query(model.MenuItem).filter(model.MenuItem.id == menu_item_id).first()
    if menu_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item id not found!")
    return menu_item

def update(db: Session, menu_item_id: int, menu_item: schema.MenuItemUpdate):
    menu_item = db.query(model.MenuItem).filter(model.MenuItem.id == menu_item_id).first()
    if menu_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item id not found!")
    for var, value in vars(menu_item).items():
        setattr(menu_item, var, value) if value else None
    db.commit()
    db.refresh(menu_item)
    return menu_item

def delete(db: Session, menu_item_id: int):
    menu_item = db.query(model.MenuItem).filter(model.MenuItem.id == menu_item_id).first()
    if menu_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item id not found!")
    db.delete(menu_item)
    db.commit()
    return menu_item