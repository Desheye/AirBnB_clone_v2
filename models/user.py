#!/usr/bin/python3
"""This module defines the User class."""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.place import Place
from models.review import Review

class User(BaseModel, Base):
    """This class represents a user in the system.

    Attributes:
        email: The email address of the user.
        password: The password of the user's account.
        first_name: The first name of the user.
        last_name: The last name of the user.
    """
    __tablename__ = "users"
    email = Column(String(128), nullable=False)
    first_name = Column(String(128))
    last_name = Column(String(128))
    password = Column(String(128), nullable=False)
    places = relationship("Place", cascade='all, delete, delete-orphan',
                          backref="user")
    reviews = relationship("Review", cascade='all, delete, delete-orphan',
                           backref="user")

