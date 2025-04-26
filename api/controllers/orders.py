from sqlalchemy.orm import Session
from sqlalchemy import select, join
import datetime
from fastapi import HTTPException, status, Response, Depends
from ..models import orders as model
from ..schemas import orders as schema
from sqlalchemy.exc import SQLAlchemyError

from ..controllers import order_details as details_controller
from ..schemas import order_details as details_schema
from ..models import order_details as details_model
from ..models import menu as menu_model
from ..models import recipes as recipe_model
from ..models import resources as resource_model


def create(db: Session, request):
    #Checking for sufficient ingredients
    requested_resources = {}
    checked_menu_items = []
    for requested_menu_item, requested_menu_item_amount in zip(request.order_details, request.item_amounts):
        #check if requested menu_item has already been checked
        if requested_menu_item in checked_menu_items:
            continue
        
        #Query 1, retrieve the needed amount for each recipe item.
        stm1 = (
            select(recipe_model.Recipe.amount)
            .where(recipe_model.Recipe.menu_item_id == requested_menu_item)
            .distinct())
        #Query 2, retrieve the id's and amounts for each resource needed.
        stmt2 = (
            select(resource_model.Resource.id, resource_model.Resource.amount)
            .select_from(recipe_model.Recipe)
            .where(recipe_model.Recipe.menu_item_id == requested_menu_item)
            .distinct()
        )
        needed_recipe_amounts = db.execute(stm1).all()
        resources = db.execute(stmt2).all()
        for amount, needed_resource in zip(needed_recipe_amounts, resources):
            #Check if the current resource has been checked previously.
            if(needed_resource[0] in requested_resources):
                requested_resources[needed_resource[0]] += amount[0] * requested_menu_item_amount
            else:
                requested_resources[needed_resource[0]] = amount[0] * requested_menu_item_amount
            
            #Check if we have enough of that resource for the order.
            if(requested_resources[needed_resource[0]] > needed_resource[1]):  
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= f"Not enough of resource id {needed_resource[0]} for this order!")
            else:
                #Update resource amounts accordingly.
                resource_to_update = db.query(model.Order).filter(resource_model.Resource.id == needed_resource[0])
                resource_to_update.update({resource_model.Resource.amount: resource_model.Resource.amount - requested_resources[needed_resource[0]]}, synchronize_session=False)
    db.commit()


    new_item = model.Order(
        customer_name=request.customer_name,
        description=request.description,
        status=request.status,
        type=request.type,

        #order_date=datetime.datetime.now(),
        promotion_code=request.promotion_code,
        order_date=datetime.datetime.now()

    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)


        order_price = 0
        for menu_item_number, amount in zip(request.order_details, request.item_amounts):
            #create a new order detail for each item in the order
            print(f"making detail for {menu_item_number} Amount: {amount}")
            detail = details_schema.OrderDetailCreate(
                order_id = str(new_item.id),
                menu_item_id = str(menu_item_number),
                amount = str(amount)
            )
            details_controller.create(db, detail)

            #sum up the price of each order detail
            result = db.query(menu_model.MenuItem).filter(menu_model.MenuItem.id == menu_item_number).first()
            order_price += result.price * amount

        #update the order object with the total price of all the items
        update_price = schema.OrderUpdate(
            totalPrice=order_price
        )
        update(db, new_item.id, update_price)


    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    
    return new_item

# Method to apply promotion to an order
def apply_promotion(db: Session, order_id: int, promotion_code: str, order_price: float):
    try:
        # Fetch the promotion based on the provided code
        promo = db.query(model.Promotion).filter(model.Promotion.code == promotion_code).first()

        if not promo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion not found!")

        # Check if the promotion is active and valid
        if not promo.is_active or not promo.check_expiration():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Promotion is expired or inactive!")

        # Apply the discount to the order price
        discount = promo.discount_percent / 100  # Assuming the discount is stored as a percentage
        order_price *= (1 - discount)

    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return order_price

def read_all(db: Session):
    try:
        result = db.query(model.Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

def read_by_date(db: Session, startDate: str, endDate: str):
    try:
        result = db.query(model.Order).filter(model.Order.order_date < endDate).filter(model.Order.order_date > startDate)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id).first()
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()

def update_status(db: Session, item_id: int, new_status: str):
    update_object = schema.OrderUpdate(
        status=new_status
    )

    if new_status == "Elevate":
        order = db.query(model.Order).filter(model.Order.id == item_id).first()
        old_status = order.status

        match(old_status):
            case "Received":
                update_object = schema.OrderUpdate(status="Finished")
            case "Finished":
                update_object = schema.OrderUpdate(status="Served")

    
    return update(db, item_id, update_object)





def delete(db: Session, item_id):
    try:
        #delete child order_details first
        details_controller.delete_by_order(db, item_id)

        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
