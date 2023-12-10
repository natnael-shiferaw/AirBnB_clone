#!/usr/bin/python3
"""This python file defines a class called BaseModel that is
used as the base model for this project."""

from datetime import datetime
from models import storage
import uuid


class BaseModel:

    """This Class is used as a parent class from which
    every other classes will inherit"""

    def __init__(self, *args, **kwargs):
        """This method is used to initialize instance attributes.

        Args:
            - *args: a tuple of arguments
            - **kwargs: represents pairs of keyword arguments
        """

        if kwargs == {} and kwargs is None:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

        else:
            for key in kwargs:
                if key == "created_at":
                    self.__dict__["created_at"] = datetime.strptime(
                        kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
                elif key == "updated_at":
                    self.__dict__["updated_at"] = datetime.strptime(
                        kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    self.__dict__[key] = kwargs[key]

    def __str__(self):
        """This method is used to return
        the official string representation"""

        return f"[{type(self).__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """This method is used to update the attribute(updated_at)
        which is a public instance."""

        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """This method is used to return a dictionary
        that contains all the key-value pairs of __dict__"""

        MyDict = self.__dict__.copy()
        MyDict["__class__"] = type(self).__name__
        MyDict["created_at"] = MyDict["created_at"].isoformat()
        MyDict["updated_at"] = MyDict["updated_at"].isoformat()
        return MyDict
