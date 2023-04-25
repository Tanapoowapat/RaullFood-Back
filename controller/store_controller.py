from model import models
from . import location_controller
from schemas import schemas
from sqlalchemy.orm import Session
from fastapi import HTTPException


# CREATE
def create_store(db: Session, store: schemas.StoreCreate):
    location = location_controller.get_location_by_id(db, location_id=store.location_id)
    if location is None:
        return None
    db_store = models.Store_Model(store_name=store.store_name, location_id=store.location_id)
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store

# READ
def get_all_stores(db: Session):
    return db.query(models.Store_Model).all()

def get_store_by_id(db: Session, store_id: int):
    store =  db.query(models.Store_Model).filter(models.Store_Model.store_id == store_id).first()
    if store is None:
        raise HTTPException(status_code=404, detail="Store Not Found")
    return store

# UPDATE
def update_store(db: Session, store_id: int, store: schemas.Store):
    db_store = get_store_by_id(db, store_id=store_id)
    if not db_store:
        return None
    if store.location_id:
        db_location = db.query(models.Location_Model).filter(models.Location_Model.location_id == store.location_id).first()
        if not db_location:
            raise HTTPException(status_code=404, detail="Location Not Found")
        db_store.location = db_location
    if store.store_name:
        db_store.store_name = store.store_name
    db.commit()
    db.refresh(db_store)
    return db_store

# DELETE
def delete_store(db: Session, store_id: int):
    db_store = get_store_by_id(db, store_id=store_id)
    if not db_store:
        return None
    db.delete(db_store)
    db.commit()
    return db_store