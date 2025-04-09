from sqlalchemy.orm import Session
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
    return db.query(model.MenuItem).filter(model.MenuItem.id == menu_item_id).first()

def update(db: Session, menu_item_id: int, menu_item: schema.MenuItemUpdate):
    db_menu_item = db.query(model.MenuItem).filter(model.MenuItem.id == menu_item_id).first()
    if db_menu_item is None:
        return None
    for var, value in vars(menu_item).items():
        setattr(db_menu_item, var, value) if value else None
    db.commit()
    db.refresh(db_menu_item)
    return db_menu_item

def delete(db: Session, menu_item_id: int):
    db_menu_item = db.query(model.MenuItem).filter(model.MenuItem.id == menu_item_id).first()
    if db_menu_item is None:
        return None
    db.delete(db_menu_item)
    db.commit()
    return db_menu_item