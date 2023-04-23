from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
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
