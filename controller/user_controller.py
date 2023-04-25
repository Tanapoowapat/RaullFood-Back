from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from config import SECRET_KEY
from model import models
from schemas import schemas

SECRET_KEY = SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, user_id: int):
    return db.query(models.UsersModel).filter(models.UsersModel.id == user_id).first()


def get_user_by_username(db: Session, username:str):
    return db.query(models.UsersModel).filter(models.UsersModel.username == username).first()

def get_users(db: Session, skip: int=0, limit: int=100):
    return db.query(models.UsersModel).offset(skip).limit(limit).all()

def auth_user(db: Session, username:str, password:str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)

def create_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_password_hash(password):
    return pwd_context.hash(password)

#to decode jwt
def decode_token(token: str):
    try:
        decode_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decode_token
    except:
        return

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.UsersModel(username=user.username, password=hashed_password, email=user.email, contact=user.contact)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user