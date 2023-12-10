#!/usr/bin/python3
"""This init python file is used to initialize the package."""

from models.engine.file_storage import FileStorage
storage = FileStorage()
storage.reload()
