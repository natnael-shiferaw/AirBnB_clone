#!/usr/bin/python3
"""This module is a unittest module used for testing
all the edge cases of the BaseModel Class which is
used as the base for the other classes."""
import unittest
import json
import uuid
from datetime import datetime
import time
import re
import os

from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models import storage



class TestBaseModel(unittest.TestCase):

    """This class is used for testing the edge Cases
    for the BaseModel class."""

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

    def test_baseModel_class_instantiation(self):
        """This method is used for testing the
        instantiation of BaseModel class."""

        ins = BaseModel()
        self.assertEqual(str(type(ins)), "<class 'models.base_model.BaseModel'>")
        self.assertIsInstance(ins, BaseModel)
        self.assertTrue(issubclass(type(ins), BaseModel))

    def test_baseModel_class_attributes(self):
        """This method is used for testing the
        attributes of BaseModel class."""

        attributes = storage.attributes()["BaseModel"]
        ins = BaseModel()
        for key, value in attributes.items():
            self.assertTrue(hasattr(ins, key))
            self.assertEqual(type(getattr(ins, key, None)), value)

    def test_baseModel_init_no_args(self):
        """This method is used for testing the
        __init__ with no arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as e:
            BaseModel.__init__()
        msg = "__init__() missing 1 required positional argument: 'self'"
        self.assertEqual(str(e.exception), msg)

    def test_baseModel_init_many_args(self):
        """This method is used for testing the
        __init__ with many arguments."""
        self.resetStorage()
        args = [n for n in range(1000)]
        ins = BaseModel(0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        ins = BaseModel(*args)


    def test_baseModel_datetime_creation(self):
        """This method is used for testing whether the attributes
        updated_at & created_at are current at creation or not."""
        current_date = datetime.now()
        ins = BaseModel()
        diff = ins.updated_at - ins.created_at
        self.assertTrue(abs(diff.total_seconds()) < 0.01)
        diff = ins.created_at - current_date
        self.assertTrue(abs(diff.total_seconds()) < 0.1)

    def test_baseModel_unique_id(self):
        """This method is used for testing for unique user ids."""

        ins = [BaseModel().id for n in range(1000)]
        self.assertEqual(len(set(ins)), len(ins))

    def test_baseModel_save_method(self):
        """This mehtod is used for testing the public instance method save()."""

        ins = BaseModel()
        time.sleep(0.5)
        current_date = datetime.now()
        ins.save()
        diff = ins.updated_at - current_date
        self.assertTrue(abs(diff.total_seconds()) < 0.01)

    def test_baseModel_str_method(self):
        """This method is used for testing the __str__ method."""
        ins = BaseModel()
        rex = re.compile(r"^\[(.*)\] \((.*)\) (.*)$")
        res = rex.match(str(ins))
        self.assertIsNotNone(res)
        self.assertEqual(res.group(1), "BaseModel")
        self.assertEqual(res.group(2), ins.id)
        s = res.group(3)
        s = re.sub(r"(datetime\.datetime\([^)]*\))", "'\\1'", s)
        d_1 = json.loads(s.replace("'", '"'))
        d_2 = ins.__dict__.copy()
        d_2["created_at"] = repr(d_2["created_at"])
        d_2["updated_at"] = repr(d_2["updated_at"])
        self.assertEqual(d_1, d_2)

    def test_baseModel_to_dict_method(self):
        """This method is used for testing the to_dict method."""

        ins = BaseModel()
        ins.name = "Sarah"
        ins.age = 21
        d = ins.to_dict()
        self.assertEqual(d["id"], ins.id)
        self.assertEqual(d["__class__"], type(ins).__name__)
        self.assertEqual(d["created_at"], ins.created_at.isoformat())
        self.assertEqual(d["updated_at"], ins.updated_at.isoformat())
        self.assertEqual(d["name"], ins.name)
        self.assertEqual(d["age"], ins.age)

    def test_baseModel_to_dict_no_args(self):
        """This method is used for testing the to_dict method with no arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as err:
            BaseModel.to_dict()
        msg = "to_dict() missing 1 required positional argument: 'self'"
        self.assertEqual(str(err.exception), msg)

    def test_baseModel_to_dict_many_args(self):
        """This method is used for testing the to_dict method
        with too many arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as e:
            BaseModel.to_dict(self, 98)
        msg = "to_dict() takes 1 positional argument but 2 were given"
        self.assertEqual(str(e.exception), msg)

    def test_baseModel_kwargs_instantiation(self):
        """This method is used for testing instantiation with **kwargs."""

        model = BaseModel()
        model.name = "Holberton"
        model.my_number = 89
        model_to_json = model.to_dict()
        new_model = BaseModel(**model_to_json)
        self.assertEqual(new_model.to_dict(), model.to_dict())

    def test_baseModel_kwargs_from_dict_instantiation(self):
        """This method is used for testing instantiation with **kwargs from custom dict."""
        my_dict = {"__class__": "BaseModel",
             "updated_at":
             datetime(2050, 12, 30, 23, 59, 59, 123456).isoformat(),
             "created_at": datetime.now().isoformat(),
             "id": uuid.uuid4(),
             "var": "foobar",
             "int": 108,
             "float": 3.14}
        ins = BaseModel(**my_dict)
        self.assertEqual(ins.to_dict(), my_dict)

    def test_baseModel_storage_save_method(self):
        """This method is used for testing storage.save()
        that's called from the save method."""
        self.resetStorage()
        ins = BaseModel()
        ins.save()
        key = "{}.{}".format(type(ins).__name__, ins.id)
        my_dict = {key: ins.to_dict()}
        self.assertTrue(os.path.isfile(FileStorage._FileStorage__file_path))
        with open(FileStorage._FileStorage__file_path,
                  "r", encoding="utf-8") as file:
            self.assertEqual(len(file.read()), len(json.dumps(my_dict)))
            file.seek(0)
            self.assertEqual(json.load(file), my_dict)

    def test_baseModel_save_method_no_args(self):
        """This method is used for testing save method with no arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as err:
            BaseModel.save()
        msg = "save() missing 1 required positional argument: 'self'"
        self.assertEqual(str(err.exception), msg)

    def test_baseModel_save_method_many_args(self):
        """This method is used for testing save method with too many arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as err:
            BaseModel.save(self, 98)
        msg = "save() takes 1 positional argument but 2 were given"
        self.assertEqual(str(err.exception), msg)


if __name__ == '__main__':
    unittest.main()
