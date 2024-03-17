#!/usr/bin/python3
"""Base model class for AirBnB."""

from datetime import datetime
import models
import uuid
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel:
    """Defines common attributes/methods for other classes."""

    created_at = Column(DateTime, nullable=False,
                        default=(datetime.utcnow()))
    id = Column(String(60), nullable=False, primary_key=True, unique=True)
    updated_at = Column(DateTime, nullable=False,
                        default=(datetime.utcnow()))

    def __init__(self, *args, **kwargs):
        """Instantiates BaseModel class."""
        if kwargs:
            for key, value in kwargs.items():
                if key in ["created_at", "updated_at"]:
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)
            if "id" not in kwargs:
                self.id = str(uuid.uuid4())
            if "created_at" not in kwargs:
                self.created_at = datetime.now()
            if "updated_at" not in kwargs:
                self.updated_at = datetime.now()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()

    def __repr__(self):
        """Returns a string representation."""
        return self.__str__()

    def __str__(self):
        """Returns a string."""
        return "[{}] ({}) {}".format(type(self).__name__, self.id,
                                     self.__dict__)

    def delete(self):
        """Deletes the current instance."""
        models.storage.delete(self)

    def save(self):
        """Updates the public instance attribute updated_at."""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Creates a dictionary of the class."""
        my_dict = dict(self.__dict__)
        my_dict["__class__"] = str(type(self).__name__)
        my_dict["created_at"] = self.created_at.isoformat()
        my_dict["updated_at"] = self.updated_at.isoformat()
        if '_sa_instance_state' in my_dict.keys():
            del my_dict['_sa_instance_state']
        return my_dict

