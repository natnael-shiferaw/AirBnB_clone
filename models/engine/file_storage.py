#!/usr/bin/python3
"""This is a module with a class called FileStorage which
is used for storage of object's data and retrieving it when
needed."""

import json
import datetime
import os


class FileStorage:

    """A class that's used for the purpose of storing
    object's data"""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """A method that returns the __objects which is
        a dictionary"""
        return FileStorage.__objects

    def new(self, obj):
        """This method is used to set in __objects the obj
        with key <obj class name>.id"""
        key = f"{type(obj).__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """ This method is used for the serialization of
        __objects to the JSON file (path: __file_path)"""
        with open(FileStorage.__file_path, "w", encoding="utf-8") as file:
            d = {key: value.to_dict()
                 for key, value in FileStorage.__objects.items()}
            json.dump(d, file)

    def classes(self):
        """This method is used to return a dictionary of
        valid classes with their references"""

        from models.amenity import Amenity
        from models.base_model import BaseModel
        from models.city import City
        from models.place import Place
        from models.review import Review
        from models.state import State
        from models.user import User

        classes = {"BaseModel": BaseModel,
                   "Amenity": Amenity,
                   "City": City,
                   "Place": Place,
                   "Review": Review,
                   "State": State,
                   "User": User}
        return classes

    def reload(self):
        """This method is used for the purpose of reloading
        the objects in storage."""
        if not os.path.isfile(FileStorage.__file_path):
            return
        with open(FileStorage.__file_path, "r", encoding="utf-8") as file:
            obj_dict = json.load(file)
            obj_dict = {key: self.classes()[value["__class__"]](**value)
                        for key, value in obj_dict.items()}
            FileStorage.__objects = obj_dict

    def attributes(self):
        """This method is used to return attributes with
        their types for classname"""

        attributes = {
            "Amenity":
                     {"name": str},
            "BaseModel":
                     {"id": str,
                      "created_at": datetime.datetime,
                      "updated_at": datetime.datetime},
            "City":
                     {"state_id": str,
                      "name": str},
            "Place":
                     {"city_id": str,
                      "user_id": str,
                      "name": str,
                      "description": str,
                      "number_rooms": int,
                      "number_bathrooms": int,
                      "max_guest": int,
                      "price_by_night": int,
                      "latitude": float,
                      "longitude": float,
                      "amenity_ids": list},
            "Review":
                     {"place_id": str,
                      "user_id": str,
                      "text": str},
            "State":
                     {"name": str},
            "User":
                     {"email": str,
                      "password": str,
                      "first_name": str,
                      "last_name": str}
        }
        return attributes
