#!/usr/bin/python3
"""Handles serialization and deserialization of instances to/from a JSON file."""
import json
import shlex
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """Serializes instances to a JSON file and deserializes JSON file to instances."""

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of objects filtered by class."""
        obj_dict = {}
        if cls:
            for key, obj in self.__objects.items():
                cls_name, obj_id = key.split(".")
                if cls_name == cls.__name__:
                    obj_dict[key] = obj
        else:
            obj_dict = self.__objects
        return obj_dict

    def new(self, obj):
        """Adds a new object to the dictionary."""
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """Serializes the objects dictionary to a JSON file."""
        serialized_objs = {}
        for key, value in self.__objects.items():
            serialized_objs[key] = value.to_dict()
        with open(self.__file_path, "w", encoding="UTF-8") as f:
            json.dump(serialized_objs, f)

    def reload(self):
        """Deserializes the JSON file to objects."""
        try:
            with open(self.__file_path, "r", encoding="UTF-8") as f:
                deserialized_objs = json.load(f)
                for key, value in deserialized_objs.items():
                    cls_name, obj_id = key.split(".")
                    value = eval(value["__class__"])(**value)
                    self.__objects[key] = value
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes an object from the dictionary."""
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            del self.__objects[key]

    def close(self):
        """Reloads objects from the JSON file."""
        self.reload()
