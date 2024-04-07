#!/usr/bin/python3
"""This module defines a DBStorage class for SQLAlchemy."""

from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """A class to manage database storage using SQLAlchemy."""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize the DBStorage instance."""
        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        db = getenv("HBNB_MYSQL_DB")
        host = getenv("HBNB_MYSQL_HOST")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(user, password, host, db),
            pool_pre_ping=True,
        )

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Return all objects of a given class."""
        obj_dict = {}
        if cls:
            if isinstance(cls, str):
                cls = eval(cls)
            query = self.__session.query(cls)
            for obj in query:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                obj_dict[key] = obj
        else:
            classes = [State, City, User, Place, Review, Amenity]
            for cls in classes:
                query = self.__session.query(cls)
                for obj in query:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """Add a new object to the database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the database."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the database."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close the session."""
        self.__session.close()
