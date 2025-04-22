from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models.menu import MenuItem
from ..schemas.menu import MenuItemCreate
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, menu_item: MenuItemCreate):
    if db.query(MenuItem).filter(MenuItem.name == menu_item.name).first() is not None:
        raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail="Menu item with that name already exists!")
    db_menu_item = MenuItem(**menu_item.model_dump())
    db.add(db_menu_item)
    db.commit()
    db.refresh(db_menu_item)
    return db_menu_item

def read_all(db: Session):
    return db.query(MenuItem).all()

def read_one(db: Session, menu_item_id: int):
    menu_item = db.query(MenuItem).filter(MenuItem.id == menu_item_id).first()
    if menu_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item id not found!")
    return menu_item

def update(db: Session, menu_item_id, request):
    try:
        menu_item = db.query(MenuItem).filter(MenuItem.id == menu_item_id)
        if not menu_item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item id not found!")
        update_data = request.dict(exclude_unset=True)
        menu_item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return menu_item.first()

def delete(db: Session, menu_item_id: int):
    menu_item = db.query(MenuItem).filter(MenuItem.id == menu_item_id).first()
    if menu_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item id not found!")
    db.delete(menu_item)
    db.commit()
    return menu_item