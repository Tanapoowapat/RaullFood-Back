from model import models
from . import user_controller, raider_controller, store_controller
from schemas import schemas
from sqlalchemy.orm import Session
from fastapi import HTTPException



"""
TODO 
CREATE METHOD FOR GET POST PUT AND DELETE FOR ORDER FOOD
"""



#GET BY ORDER NAME
def get_order_by_id(db: Session, order_id : int):
    order = db.query(models.Order).filter(models.Order.order_id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not Found!")
    return order

#get all
def get_all_orders(db:Session):
    return db.query(models.Order).all()

#get by user_id
def get_order_by_user_id(db: Session, user_id:int):
    user = user_controller.get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Users Not Found")
    order = db.query(models.Order).filter(models.Order.user_id == user.id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order Not Found")
    return order

#CREATE ORDER
def create_order(db: Session, order: schemas.OrderCreate):
    user = user_controller.get_user(db=db, user_id=order.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User Not Found")
    store = store_controller.get_store_by_id(db=db, store_id= order.store_id)
    if store is None:
        return None
    db_order = models.Order(orderDetails = order.orderDetails, store_id = store.store_id, user_id = user.id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

#UPDATE ORDER
def update_order(db: Session, order: schemas.OrderUpdate):
    db_order = get_order_by_id(db=db, order_id= order.order_id)
    if db_order is None:
        return None
    if order.raider_id:
        raider = raider_controller.get_raider_by_id(db=db, raider_id= order.raider_id)
        if raider is None:
            return None
        db_order.raider_id = raider.raider_id
    if order.orderDetails:
        db_order.orderDetails = order.orderDetails
    db.commit()
    db.refresh(db_order)
    return db_order

#DELETE
def delete_order(db : Session, order_id : int):
    db_order = get_order_by_id(db=db, order_id = order_id)
    if db_order is None:
        return None
    db.delete(db_order)
    db.commit()
    return db_order
