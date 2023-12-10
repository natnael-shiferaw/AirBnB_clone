#!/usr/bin/python3
"""This module is a unittest module used for testing
all the edge cases of the Amenity Class which is used
to manage amenity objects."""

from models.amenity import Amenity
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models import storage

import unittest
import json
import time
from datetime import datetime
import re
import os


class TestAmenity(unittest.TestCase):

    """This class is used for testing the edge Cases
    for the Amenity class."""

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

    def test_amenity_class_instantiation(self):
        """This method is used for testing the
        instantiation of Amenity class."""

        ins = Amenity()
        self.assertEqual(str(type(ins)), "<class 'models.amenity.Amenity'>")
        self.assertIsInstance(ins, Amenity)
        self.assertTrue(issubclass(type(ins), BaseModel))

    def test_amenity_class_attributes(self):
        """This method is used for testing the
        attributes of Amenity class."""
        attributes = storage.attributes()["Amenity"]
        a = Amenity()
        for key, value in attributes.items():
            self.assertTrue(hasattr(a, key))
            self.assertEqual(type(getattr(a, key, None)), value)


if __name__ == "__main__":
    unittest.main()
