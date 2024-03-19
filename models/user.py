#!/usr/bin/python3
"""Defines the User class."""
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.place import Place
from models.review import Review


class User(BaseModel, Base):
    """Represents a user in the database.
    Attributes:
        email: The user's email address.
        password: The user's password for login.
        first_name: The user's first name.
        last_name: The user's last name.
    """

    __tablename__ = "users"
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128))
    last_name = Column(String(128))
    places = relationship("Place", cascade="all, delete, delete-orphan", backref="user")
    reviews = relationship(
        "Review", cascade="all, delete, delete-orphan", backref="user"
    )
