#!/usr/bin/python3
"""This module defines the Review class."""
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float


class Review(BaseModel, Base):
    """This class represents a review in the system.

    Attributes:
        place_id: The id of the place being reviewed.
        user_id: The id of the user who wrote the review.
        text: The content of the review.
    """
    __tablename__ = "reviews"
    text = Column(String(1024), nullable=False)
    place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
