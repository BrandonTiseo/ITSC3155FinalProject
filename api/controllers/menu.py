from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models.menu import MenuItem
from sqlalchemy.exc import SQLAlchemyError

from ..controllers import recipes as recipe_controller
from ..schemas import recipes as recipe_schema

def create(db: Session, request):
    if db.query(MenuItem).filter(MenuItem.name == request.name).first() is not None:
        raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail="Menu Item with that name already exists!" )
    new_menu_item = MenuItem(
        name = request.name,
        price = request.price,
        calories = request.calories,
        category = request.category
    )

    try:
        db.add(new_menu_item)
        db.commit()
        db.refresh(new_menu_item)


        for resource_item_number, resource_amount in zip(request.recipe_items, request.recipe_amounts):
            recipe = recipe_schema.RecipeCreate(
                menu_item_id = str(new_menu_item.id),
                resource_id = str(resource_item_number),
                amount = str(resource_amount)
            )
            recipe_controller.create(db, recipe)
            
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    
    return new_menu_item


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
    recipe_controller.delete_by_menu_item(db, menu_item_id)
    
    menu_item = db.query(MenuItem).filter(MenuItem.id == menu_item_id).first()
    if menu_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item id not found!")
    db.delete(menu_item)
    db.commit()
    return menu_item


def search_by_category(db: Session, category: str):
    search_result = db.query(MenuItem).filter(MenuItem.category.ilike(f"%{category}%")).all()
    
    if not search_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No menu items found for this category.")
    
    return search_result