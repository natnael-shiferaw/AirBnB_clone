#!/usr/bin/python3
"""This is a module that creates a class called
City that inherits from the BaseModel class"""

from models.base_model import BaseModel


class City(BaseModel):
    """A class that's used to manage city objects
    and inherits attributes from the BaseModel class"""

    state_id = ""
    name = ""
