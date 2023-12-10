#!/usr/bin/python3
"""This module is a unittest module used for testing
all the edge cases of the State Class which is used
to manage state objects."""

from models.state import State
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models import storage

import unittest
import json
from datetime import datetime
import time
import re
import os


class TestState(unittest.TestCase):

    """This class is used for testing the edge Cases
    for the State class."""

    def setUp(self):
        """This method is used for setting up test methods."""
        pass

    def tearDown(self):
        """This method is used for tearing down test methods."""
        self.resetStorage()
        pass

    def resetStorage(self):
        """This method is used for resetting the data in FileStorage."""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_state_class_instantiation(self):
        """This method is used for testing the
        instantiation of State class."""

        ins = State()
        self.assertEqual(str(type(ins)), "<class 'models.state.State'>")
        self.assertIsInstance(ins, State)
        self.assertTrue(issubclass(type(ins), BaseModel))

    def test_state_class_attributes(self):
        """This method is used for testing the
        attributes of State class."""
        attributes = storage.attributes()["State"]
        ins = State()
        for key, value in attributes.items():
            self.assertTrue(hasattr(ins, key))
            self.assertEqual(type(getattr(ins, key, None)), value)


if __name__ == "__main__":
    unittest.main()
