from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base



class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    access_token = Column(String, unique=True, nullable=True)
    refresh_token = Column(String, unique=True, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("UsersModel", back_populates="tokens")

class UsersModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String, unique=True)
    contact = Column(String, unique=True)
    access_token = Column(String, unique=True, nullable=True)
    refresh_token = Column(String, unique=True, nullable=True)

    tokens = relationship("Token", back_populates="user")
    order = relationship("Order", back_populates="user")
    raider = relationship("RaiderModel", back_populates="user")

class RaiderModel(Base):
    __tablename__ = "raider"

    raider_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("UsersModel", back_populates="raider")
    order = relationship("Order", back_populates="raider")

class Order(Base):
    __tablename__ = "order"

    order_id = Column(Integer, primary_key=True, index=True)
    orderDetails = Column(String, unique=True, nullable=True)
    store_id = Column(String, unique=True, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    raider_id = Column(Integer, ForeignKey("raider.raider_id"))

    raider = relationship("RaiderModel", back_populates="order")
    user = relationship("UsersModel", back_populates="order")

class Location_Model(Base):
    __tablename__ = "location"
    location_id = Column(Integer, primary_key=True, index=True)
    location_name = Column(String, unique=True, index=True)

    store = relationship("Store_Model", back_populates="location")

class Store_Model(Base):
    __tablename__ = "store"
    store_id = Column(Integer, primary_key=True, index=True)
    store_name = Column(String, unique=True, index=True)
    location_id = Column(Integer, ForeignKey("location.location_id"))

    location = relationship("Location_Model", back_populates="store")
