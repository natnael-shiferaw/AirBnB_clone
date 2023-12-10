#!/usr/bin/python3
"""This is a module that creates a class called
User that inherits from the BaseModel class"""
from models.base_model import BaseModel


class User(BaseModel):
    """A class that's used to manage user objects
    and inherits attributes from the BaseModel class"""

    email = ""
    password = ""
    first_name = ""
    last_name = ""
