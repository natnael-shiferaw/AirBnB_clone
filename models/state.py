#!/usr/bin/python3
"""This is a module that creates a class called
State that inherits from the BaseModel class"""

from models.base_model import BaseModel


class State(BaseModel):
    """A class that's used to manage state objects
    and inherits attributes from the BaseModel class"""

    name = ""
