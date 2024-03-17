#!/usr/bin/python3
"""This module defines the Place class."""
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Table, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv
import models

place_amenity = Table("place_amenity", Base.metadata,
                      Column("place_id", String(60),
                             ForeignKey("places.id"),
                             primary_key=True,
                             nullable=False),
                      Column("amenity_id", String(60),
                             ForeignKey("amenities.id"),
                             primary_key=True,
                             nullable=False))

class Place(BaseModel, Base):
    """This class represents a place in the system.

    Attributes:
        city_id: The id of the city where the place is located.
        user_id: The id of the user who owns the place.
        name: The name of the place.
        description: A description of the place.
        number_rooms: The number of rooms in the place.
        number_bathrooms: The number of bathrooms in the place.
        max_guest: The maximum number of guests the place can accommodate.
        price_by_night: The price per night for staying at the place.
        latitude: The latitude coordinate of the place.
        longitude: The longitude coordinate of the place.
        amenity_ids: A list of ids of amenities associated with the place.
    """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship("Review", cascade='all, delete, delete-orphan',
                               backref="place")
        amenities = relationship("Amenity", secondary=place_amenity,
                                 viewonly=False,
                                 back_populates="place_amenities")
    else:
        @property
        def reviews(self):
            """Returns a list of reviews associated with the place."""
            var = models.storage.all()
            review_list = []
            result = []
            for key in var:
                review = key.replace('.', ' ')
                review = shlex.split(review)
                if (review[0] == 'Review'):
                    review_list.append(var[key])
            for element in review_list:
                if (element.place_id == self.id):
                    result.append(element)
            return result

        @property
        def amenities(self):
            """Returns a list of amenity ids associated with the place."""
            return self.amenity_ids

        @amenities.setter
        def amenities(self, obj=None):
            """Appends amenity ids to the attribute."""
            if type(obj) is Amenity and obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)

