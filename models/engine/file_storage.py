#!/usr/bin/python3
"""This module defines the FileStorage class for AirBnB project."""
import json
# from models.user import User
from models.state import State
# from models.city import City
# from models.amenity import Amenity
# from models.place import Place
# from models.review import Review
# import shlex


class FileStorage:
    """This class serializes JSON file to instances."""
    _file_path = "file.json"
    _objects = {}

    def all(self, cls=None):
        """Returns a dictionary containing all objects."""
        result = {}
        if cls:
            for key, value in self._objects.items():
                partition = key.split('.')
                if partition[0] == cls.__name__:
                    result[key] = value
            return result
        else:
            return self._objects

    def new(self, obj):
        """Adds a new object to the storage."""
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            self._objects[key] = obj

    def save(self):
        """Serializes the objects to the JSON file."""
        my_dict = {}
        for key, value in self._objects.items():
            my_dict[key] = value.to_dict()
        with open(self._file_path, 'w', encoding="UTF-8") as f:
            json.dump(my_dict, f)

    def reload(self):
        """Deserializes the JSON file to objects."""
        try:
            with open(self._file_path, 'r', encoding="UTF-8") as f:
                for key, value in json.load(f).items():
                    value = eval(value["__class__"])(**value)
                    self._objects[key] = value
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes an object from the storage."""
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            del self._objects[key]

    def delete_state(self, state_obj):
        """Deletes a State object from the storage."""
        if isinstance(state_obj, State):
            key = "{}.{}".format(type(state_obj).__name__, state_obj.id)
            del self._objects[key]
        else:
            # Optionally handle cases where a non-State object is passed
            print("Only State objects can be deleted using delete_state.")

    def close(self):
        """Reloads the data from the JSON file."""
        self.reload()
