#!/usr/bin/python3
"""This module is a unittest module used for testing
all the edge cases of the FileStorage class which is
used for the purpose of storing data."""

from models.engine.file_storage import FileStorage
from models import storage
from models.base_model import BaseModel

import unittest
import json
from datetime import datetime
import time
import re
import os


class TestFileStorage(unittest.TestCase):
    """This class is used for testing the edge Cases
    for the FileStorage class."""

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

    def test_FileStorage_class_instantiation(self):
        """This method is used for testing the
        instantiation of storage class."""
        self.assertEqual(type(storage).__name__, "FileStorage")

    def test_FileStorage_class_attributes(self):
        """This method is used for testing the
        attributes of FileStorage class."""
        self.resetStorage()
        self.assertTrue(hasattr(FileStorage, "_FileStorage__file_path"))
        self.assertTrue(hasattr(FileStorage, "_FileStorage__objects"))
        self.assertEqual(getattr(FileStorage, "_FileStorage__objects"), {})

    def test_FileStorage_init_no_args(self):
        """This method is used for testing the
        __init__ with no arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as err:
            FileStorage.__init__()
        msg = "descriptor '__init__' of 'object' object needs an argument"
        self.assertEqual(str(err.exception), msg)

    def test_FileStorage_init_many_args(self):
        """This method is used for testing the
        __init__ with many arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as err:
            ins = FileStorage(0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        msg = "object() takes no parameters"
        self.assertEqual(str(err.exception), msg)

    def helper_test_all_method(self, class_name):
        """This method helps to test the all method for classname."""
        self.resetStorage()
        self.assertEqual(storage.all(), {})

        ins = storage.classes()[class_name]()
        storage.new(ins)
        key = f"{type(ins).__name__}.{ins.id}"
        self.assertTrue(key in storage.all())
        self.assertEqual(storage.all()[key], ins)

    def test_baseModel_all_method(self):
        """This method is used to test the all method for BaseModel."""
        self.helper_test_all_method("BaseModel")

    def test_user_all_method(self):
        """This method is used to test the all method for User."""
        self.helper_test_all_method("User")

    def test_state_all_method(self):
        """This method is used to test the all method for State."""
        self.helper_test_all_method("State")

    def test_city_all_method(self):
        """This method is used to test the all method for City."""
        self.helper_test_all_method("City")

    def test_amenity_all_method(self):
        """This method is used to test the all method for Amenity."""
        self.helper_test_all_method("Amenity")

    def test_place_all_method(self):
        """This method is used to test the all method for Place."""
        self.helper_test_all_method("Place")

    def test_review_all_method(self):
        """This method is used to test the all method for Review."""
        self.helper_test_all_method("Review")

    def helper_test_all_method_many_obj(self, class_name):
        """This method helps to test the all method
        with many objects for classname."""
        self.resetStorage()
        self.assertEqual(storage.all(), {})

        cls = storage.classes()[class_name]
        objects = [cls() for n in range(1000)]
        [storage.new(obj) for obj in objects]
        self.assertEqual(len(objects), len(storage.all()))
        for obj in objects:
            key = f"{type(obj).__name__}.{obj.id}"
            self.assertTrue(key in storage.all())
            self.assertEqual(storage.all()[key], obj)

    def test_baseModel_all_method_many_obj(self):
        """This method tests the all method with many objects for BaseModel."""
        self.helper_test_all_method_many_obj("BaseModel")

    def test_user_all_method_many_obj(self):
        """This method tests the all method with many objects for User."""
        self.helper_test_all_method_many_obj("User")

    def test_state_all_method_many_obj(self):
        """This method tests the all method with many objects for State."""
        self.helper_test_all_method_many_obj("State")

    def test_city_all_method_many_obj(self):
        """This method tests the all method with many objects for City."""
        self.helper_test_all_method_many_obj("City")

    def test_amenity_all_method_many_obj(self):
        """This method tests the all method with many objects for Amenity."""
        self.helper_test_all_method_many_obj("Amenity")

    def test_place_all_method_many_obj(self):
        """This method tests the all method with many objects for Place."""
        self.helper_test_all_method_many_obj("Place")

    def test_review_all_method_many_obj(self):
        """This method tests the all method with many objects for Review."""
        self.helper_test_all_method_many_obj("Review")

    def test_all_method_with_no_args(self):
        """This method tests the all method with no arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as err:
            FileStorage.all()
        msg = "all() missing 1 required positional argument: 'self'"
        self.assertEqual(str(err.exception), msg)

    def test_all_method_with_many_args(self):
        """This method tests the all method with too many arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as err:
            FileStorage.all(self, 98)
        msg = "all() takes 1 positional argument but 2 were given"
        self.assertEqual(str(err.exception), msg)

    def helper_test_new_method(self, class_name):
        """This method helps to test the new method for classname."""
        self.resetStorage()
        cls = storage.classes()[class_name]
        obj = cls()
        storage.new(obj)
        key = f"{type(obj).__name__}.{obj.id}"
        self.assertTrue(key in FileStorage._FileStorage__objects)
        self.assertEqual(FileStorage._FileStorage__objects[key], obj)

    def test_baseModel_new_method(self):
        """This method helps to test the new method for BaseModel."""
        self.helper_test_new_method("BaseModel")

    def test_user_new_method(self):
        """This method helps to test the new method for User."""
        self.helper_test_new_method("User")

    def test_state_new_method(self):
        """This method helps to test the new method for State."""
        self.helper_test_new_method("State")

    def test_city_new_method(self):
        """This method helps to test the new method for City."""
        self.helper_test_new_method("City")

    def test_amenity_new_method(self):
        """This method helps to test the new method for Amenity."""
        self.helper_test_new_method("Amenity")

    def test_place_new_method(self):
        """This method helps to test the new method for Place."""
        self.helper_test_new_method("Place")

    def test_review_new_method(self):
        """This method helps to test the new method for Review."""
        self.helper_test_new_method("Review")

    def test_new_method_with_no_args(self):
        """This method helps to test the new method with no arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as err:
            storage.new()
        msg = "new() missing 1 required positional argument: 'obj'"
        self.assertEqual(str(err.exception), msg)

    def test_new_method_with_many_args(self):
        """This method helps to test the new method with too many arguments."""
        self.resetStorage()
        ins = BaseModel()
        with self.assertRaises(TypeError) as err:
            storage.new(ins, 98)
        msg = "new() takes 2 positional arguments but 3 were given"
        self.assertEqual(str(err.exception), msg)

    def helper_test_save_method(self, class_name):
        """This method helps to test the save method for classname."""
        self.resetStorage()
        cls = storage.classes()[class_name]
        obj = cls()
        storage.new(obj)
        key = f"{type(obj).__name__}.{obj.id}"
        storage.save()
        self.assertTrue(os.path.isfile(FileStorage._FileStorage__file_path))
        my_dict = {key: obj.to_dict()}
        with open(FileStorage._FileStorage__file_path,
                  "r", encoding="utf-8") as file:
            self.assertEqual(len(file.read()), len(json.dumps(my_dict)))
            file.seek(0)
            self.assertEqual(json.load(file), my_dict)

    def test_baseModel_save_method(self):
        """This method helps to test the save method for BaseModel."""
        self.helper_test_save_method("BaseModel")

    def test_user_save_method(self):
        """This method helps to test the save method for User."""
        self.helper_test_save_method("User")

    def test_state_save_method(self):
        """This method helps to test the save method for State."""
        self.helper_test_save_method("State")

    def test_city_save_method(self):
        """This method helps to test the save method for City."""
        self.helper_test_save_method("City")

    def test_amenity_save_method(self):
        """This method helps to test the save method for Amenity."""
        self.helper_test_save_method("Amenity")

    def test_place_save_method(self):
        """This method helps to test the save method for Place."""
        self.helper_test_save_method("Place")

    def test_review_save_method(self):
        """This method helps to test the save method for Review."""
        self.helper_test_save_method("Review")

    def test_save_method_with_no_args(self):
        """This method helps to test the save method with no arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as err:
            FileStorage.save()
        msg = "save() missing 1 required positional argument: 'self'"
        self.assertEqual(str(err.exception), msg)

    def test_save_method_with_many_args(self):
        """This method helps to test the save method with too many arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as err:
            FileStorage.save(self, 98)
        msg = "save() takes 1 positional argument but 2 were given"
        self.assertEqual(str(err.exception), msg)

    def helper_test_reload_method(self, class_name):
        """This method helps to test the reload method for classname."""
        self.resetStorage()
        storage.reload()
        self.assertEqual(FileStorage._FileStorage__objects, {})
        cls = storage.classes()[class_name]
        obj = cls()
        storage.new(obj)
        key = f"{type(obj).__name__}.{obj.id}"
        storage.save()
        storage.reload()
        self.assertEqual(obj.to_dict(), storage.all()[key].to_dict())

    def test_baseModel_reload_method(self):
        """This method helps to test the reload method for BaseModel."""
        self.helper_test_reload_method("BaseModel")

    def test_user_reload_method(self):
        """This method helps to test the reload method for User."""
        self.helper_test_reload_method("User")

    def test_state_reload_method(self):
        """This method helps to test the reload method for State."""
        self.helper_test_reload_method("State")

    def test_city_reload_method(self):
        """This method helps to test the reload method for City."""
        self.helper_test_reload_method("City")

    def test_amenity_reload_method(self):
        """This method helps to test the reload method for Amenity."""
        self.helper_test_reload_method("Amenity")

    def test_place_reload_method(self):
        """This method helps to test the reload method for Place."""
        self.helper_test_reload_method("Place")

    def test_review_reload_method(self):
        """This method helps to test the reload method for Review."""
        self.helper_test_reload_method("Review")

    def helper_test_reload_method_mismatch(self, class_name):
        """This method helps to test the reload method mismatch for classname."""
        self.resetStorage()
        storage.reload()
        self.assertEqual(FileStorage._FileStorage__objects, {})

        cls = storage.classes()[class_name]
        obj = cls()
        storage.new(obj)
        key = f"{type(obj).__name__}.{obj.id}"
        storage.save()
        obj.name = "Laura"
        storage.reload()
        self.assertNotEqual(obj.to_dict(), storage.all()[key].to_dict())

    def test_baseModel_reload_method_mismatch(self):
        """This method helps to test the reload method mismatch for BaseModel."""
        self.helper_test_reload_method_mismatch("BaseModel")

    def test_user_reload_method_mismatch(self):
        """This method helps to test the reload method mismatch for User."""
        self.helper_test_reload_method_mismatch("User")

    def test_state_reload_method_mismatch(self):
        """This method helps to test the reload method mismatch for State."""
        self.helper_test_reload_method_mismatch("State")

    def test_city_reload_method_mismatch(self):
        """This method helps to test the reload method mismatch for City."""
        self.helper_test_reload_method_mismatch("City")

    def test_amenity_reload_method_mismatch(self):
        """This method helps to test the reload method mismatch for Amenity."""
        self.helper_test_reload_method_mismatch("Amenity")

    def test_place_reload_method_mismatch(self):
        """Tests reload_mismatch() method for Place."""
        self.helper_test_reload_method_mismatch("Place")

    def test_review_reload_method_mismatch(self):
        """This method helps to test the reload method mismatch for Review."""
        self.helper_test_reload_method_mismatch("Review")

    def test_reload_method_with_no_args(self):
        """This method helps to test the reload method with no arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as err:
            FileStorage.reload()
        msg = "reload() missing 1 required positional argument: 'self'"
        self.assertEqual(str(err.exception), msg)

    def test_reload_method_with_many_args(self):
        """This method helps to test the reload method with too many arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as err:
            FileStorage.reload(self, 98)
        msg = "reload() takes 1 positional argument but 2 were given"
        self.assertEqual(str(err.exception), msg)


if __name__ == '__main__':
    unittest.main()
