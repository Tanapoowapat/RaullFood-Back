from typing import Optional
from pydantic import BaseModel

#USER SCHEMAS
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    email: str
    contact: str

class User(UserBase):
    id: Optional[int] = None
    email: str
    contact: str

    class Config:
        orm_mode = True

#RAIDER SCHEMAS
class RaiderBase(BaseModel):
    pass


class RaiderCreate(RaiderBase):
    user_id: int


class Raider(RaiderBase):
    raider_id: Optional[int] = None
    user_id: int

    class Config:
        orm_mode = True

#ORDER SCHEMAS
class OrderBase(BaseModel):
    orderDetails: str
    store_id: int
    user_id: int
    raider_id: Optional[int] = None

class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    order_id: int
    user: User
    raider: Raider

    class Config:
        orm_mode = True

#TOKEN SCHEMAS
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

#LOCATION SCHEMAS
class LocationBase(BaseModel):
    location_name : str

class LocationUpdate(BaseModel):
    location_name : str

class LocationCreate(BaseModel):
    location_id : int


class Location(BaseModel):
    location_id : Optional[int] = None
    location_name : str

    class Config:
        orm_mode = True

#STORE SCHEMAS
class StoreBase(BaseModel):
    store_name : str
    location_id : Optional[int] = None

class StoreUpdate(BaseModel):
    store_name: Optional[str] = None
    location_id: Optional[int] = None

class StoreCreate(BaseModel):
    store_id: Optional[int] = None
    store_name: str
    location_id: int


class Store(BaseModel):
    store_id : Optional[int] = None
    store_name: str
    location_id: int
    
    class Config:
        orm_mode = True

Location.update_forward_refs()