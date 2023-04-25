from model import models
from schemas import schemas
from sqlalchemy.orm import Session
from fastapi import HTTPException

#get all
def get_location(db: Session, skip: int=0, limit: int=100):
    return db.query(models.Location_Model).offset(skip).limit(limit).all()

# GET a location by ID
def get_location_by_id(db: Session, location_id: int):
    location_id = db.query(models.Location_Model).filter(models.Location_Model.location_id == location_id).first()
    if location_id is None:
        raise HTTPException(status_code=404, detail="Location Not Found")
    return location_id

def get_location_by_name(db: Session, location_name:str):
    return db.query(models.Location_Model).filter(models.Location_Model.location_name == location_name).first()

#CREATE STORE
def create_location(db: Session, location: schemas.Location):
    db_location = models.Location_Model(**location.dict())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

#UPDATE
def update_location(db: Session, location_id: int, location: schemas.Location):
    db_location = get_location_by_id(db, location_id=location_id)
    if not db_location:
        return None
    db_location.location_name = location.location_name
    db.commit()
    db.refresh(db_location)
    return db_location

#DELETE
def delete_location(db: Session, location_id: int):
    db_location = get_location_by_id(db, location_id=location_id)
    if not location_id:
        return  None
    db.delete(db_location)
    db.commit()
    return db_location