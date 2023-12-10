#!/usr/bin/python3
"""This python file is a module that creates a class
called Amenity that inherits from the BaseModel class"""

from models.base_model import BaseModel


class Amenity(BaseModel):
    """A class that's used to manage amenity objects
    and inherits attributes from the BaseModel class"""

    name = ""
