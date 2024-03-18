#!/usr/bin/python3
"""Module for the State class"""
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
import models
from models.city import City
import shlex


class State(BaseModel, Base):
    """A class representing a state.

    Attributes:
        name: The name of the state.
    """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade='all, delete, delete-orphan',
                          backref="state")

    @property
    def cities(self):
        """Property getter that returns a list of associated cities."""
        var = models.storage.all()
        city_list = []
        result = []
        for key in var:
            city = key.replace('.', ' ')
            city = shlex.split(city)
            if city[0] == 'City':
                city_list.append(var[key])
        for elem in city_list:
            if elem.state_id == self.id:
                result.append(elem)
        return result
