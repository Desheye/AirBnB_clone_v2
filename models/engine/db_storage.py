#!/usr/bin/python3
"""This module defines the DBStorage class for SQL Alchemy."""
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
    """This class manages SQL Alchemy database storage."""
    _engine = None
    _session = None

    def __init__(self):
        """Initialize the database connection."""
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        db = getenv("HBNB_MYSQL_DB")
        host = getenv("HBNB_MYSQL_HOST")
        env = getenv("HBNB_ENV")

        self._engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                     .format(user, passwd, host, db),
                                     pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self._engine)

    def all(self, cls=None):
        """Returns a dictionary of all objects."""
        obj_dict = {}
        if cls:
            if isinstance(cls, str):
                cls = eval(cls)
            query = self._session.query(cls)
            for obj in query:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                obj_dict[key] = obj
        else:
            class_list = [State, City, User, Place, Review, Amenity]
            for cls in class_list:
                query = self._session.query(cls)
                for obj in query:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """Add a new object to the session."""
        self._session.add(obj)

    def save(self):
        """Commit changes to the database."""
        self._session.commit()

    def delete(self, obj=None):
        """Delete an object from the session."""
        if obj:
            self._session.delete(obj)

    def reload(self):
        """Configure the session and metadata."""
        Base.metadata.create_all(self._engine)
        Session = sessionmaker(bind=self._engine, expire_on_commit=False)
        self._session = scoped_session(Session)()

    def close(self):
        """Close the session."""
        self._session.close()

