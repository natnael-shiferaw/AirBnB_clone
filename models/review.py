#!/usr/bin/python3
"""This is a module that creates a class called
Review that inherits from the BaseModel class"""

from models.base_model import BaseModel


class Review(BaseModel):
    """A class that's used to manage review objects
    and inherits attributes from the BaseModel class"""

    place_id = ""
    user_id = ""
    text = ""
