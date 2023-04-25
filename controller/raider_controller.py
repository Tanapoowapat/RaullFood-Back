from model import models
from . import user_controller
from schemas import schemas
from sqlalchemy.orm import Session
from fastapi import HTTPException

#GET ALL raider
def get_all_raider(db: Session):
    return db.query(models.RaiderModel).all()

#GET BY ID
def get_raider_by_id(db: Session, raider_id: int):
    raider = db.query(models.RaiderModel).filter(models.RaiderModel.raider_id == raider_id).first()
    if raider is None:
        raise HTTPException(status_code=400, detail="raider Not Found")
    return raider

#GET BY USERID
def verify_raider(db:Session, user_id: int):
    user_id = db.query(models.RaiderModel).filter(models.RaiderModel.user_id == user_id).first()
    if user_id:
        return False
    return True


#CREATE RAIDER
def create_raider(db: Session, raider: schemas.RaiderCreate):
    user = user_controller.get_user(db, user_id=raider.user_id)
    if user is None:
        raise HTTPException(status_code=400, detail="User Not Found!")
    if not verify_raider(db, user_id=user.id):
        raise HTTPException(status_code=409, detail="Raider Already Create")
    db_raider = models.RaiderModel(user_id = raider.user_id)
    db.add(db_raider)
    db.commit()
    db.refresh(db_raider)
    return db_raider

#DELETE RAIDER
def delete_raider(db: Session, raider_id: int):
    db_raider = get_raider_by_id(db, raider_id=raider_id)
    if not db_raider:
        return None
    db.delete(db_raider)
    db.commit()
    return db_raider