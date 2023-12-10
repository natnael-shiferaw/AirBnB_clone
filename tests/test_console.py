#!/usr/bin/python3
"""This module is a unittest module used for testing
all the edge cases for the HBNBCommand class which
contains the entry point of the command interpreter."""

import unittest
from unittest.mock import patch
import datetime
import sys
import re
import os
from io import StringIO

from models.engine.file_storage import FileStorage
from console import HBNBCommand


class TestHBNBCommand(unittest.TestCase):

    """This class is used for testing the edge Cases
    for the HBNBCommand console."""

    attr_val = {
        str: "string",
        int: 42,
        float: 3.14
    }

    rest_val = {
        str: "",
        int: 0,
        float: 0.0
    }

    custom_attr_test = {
        "str_atrr": "foofoo",
        "int_atrr": 341,
        "float_atrr": 7.7
    }

    def setUp(self):
        """This method is used for setting up test methods."""
        if os.path.isfile("file.json"):
            os.remove("file.json")
        self.resetStorage()

    def resetStorage(self):
        """This method is used for resetting the data in FileStorage."""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_help_command(self):
        """This method is used for testing the help command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help")
        expected_output = """
Documented commands (type help <topic>):
========================================
EOF  all  count  create  destroy  help  quit  show  update

"""
        self.assertEqual(expected_output, f.getvalue())

    def test_help_command_for_EOF(self):
        """A method that tests the help command for EOF."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help EOF")
        expected_output = 'This method is used to handle the End Of File.\n        \n'
        self.assertEqual(expected_output, f.getvalue())

    def test_help_command_for_quit(self):
        """A method that tests the help command for quit."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help quit")
        expected_output = 'This method is a Quit command to exit the program.\n        \n'
        self.assertEqual(expected_output, f.getvalue())

    def test_help_command_for_create(self):
        """A method that tests the help command for create."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help create")
        expected_output = '''This method is used to create a new instance of BaseModel,
        saves it(to the JSON file) and prints the id.\n        \n'''
        self.assertEqual(expected_output, f.getvalue())

    def test_help_command_for_show(self):
        """A method that tests the help command for show."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help show")
        expected_output = '''This method is used for the purpose of printing
        the string representation of an instance.\n        \n'''
        self.assertEqual(expected_output, f.getvalue())

    def test_help_command_for_destroy(self):
        """A method that tests the help command for destroy."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help destroy")
        expected_output = '''This method is used for deleting an instance
        by the use of id and class name.\n        \n'''
        self.assertEqual(expected_output, f.getvalue())

    def test_help_command_for_all(self):
        """A method that tests the help command for all."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help all")
        expected_output = '''This method is used for printing all the string
        representation of every instance.\n        \n'''
        self.assertEqual(expected_output, f.getvalue())

    def test_help_command_for_count(self):
        """A method that tests the help command for count."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help count")
        expected_output = '''This method is used for counting the
        instances of a class.\n        \n'''
        self.assertEqual(expected_output, f.getvalue())

    def test_help_command_for_update(self):
        """A method that tests the help command for update."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help update")
        expected_output = '''This method is used for updating an instance
        through updation or addition of an attribute.\n        \n'''
        self.assertEqual(expected_output, f.getvalue())

    def test_do_quit_command(self):
        """This method is used for testing quit commmand."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("quit")
        msg = f.getvalue()
        self.assertTrue(len(msg) == 0)
        self.assertEqual("", msg)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("quit garbage")
        msg = f.getvalue()
        self.assertTrue(len(msg) == 0)
        self.assertEqual("", msg)

    def test_do_EOF_command(self):
        """This method is used for testing EOF commmand."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("EOF")
        msg = f.getvalue()
        self.assertTrue(len(msg) == 1)
        self.assertEqual("\n", msg)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("EOF garbage")
        msg = f.getvalue()
        self.assertTrue(len(msg) == 1)
        self.assertEqual("\n", msg)

    def test_emptyline_functionality(self):
        """This method is used for testing emptyline's functionality."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("\n")
        expected_output = ""
        self.assertEqual(expected_output, f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("                  \n")
        expected_output = ""
        self.assertEqual(expected_output, f.getvalue())

    def test_do_create_command(self):
        """This method is used for testing create command."""
        for class_name in self.classes():
            self.helper_test_for_create_command(class_name)

    def helper_test_for_create_command(self, class_name):
        """This method helps to test the create commmand."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"create {class_name}")
        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)
        key = "{}.{}".format(class_name, uid)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"all {class_name}")
        self.assertTrue(uid in f.getvalue())

    def test_create_command_with_error(self):
        """This method helps to test create command with errors."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create garbage")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

    def test_show_command(self):
        """This method helps to test show for all classes."""
        for class_name in self.classes():
            self.helper_test_for_show_command(class_name)
            self.helper_test_for_show_command_advanced(class_name)

    def helper_test_for_show_command(self, class_name):
        """This method helps to test the show command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"create {class_name}")
        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"show {class_name} {uid}")
        expected_output = f.getvalue()[:-1]
        self.assertTrue(uid in expected_output)

    def test_show_command_with_error(self):
        """This method helps to test show command with errors."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show")
        expected_msg = f.getvalue()[:-1]
        self.assertEqual(expected_msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show garbage")
        expected_msg = f.getvalue()[:-1]
        self.assertEqual(expected_msg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show BaseModel")
        expected_msg = f.getvalue()[:-1]
        self.assertEqual(expected_msg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show BaseModel 6524359")
        expected_msg = f.getvalue()[:-1]
        self.assertEqual(expected_msg, "** no instance found **")

    def helper_test_for_show_command_advanced(self, class_name):
        """This method helps to test .show() command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"create {class_name}")
        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'{class_name}.show("{uid}")')
        expected_output = f.getvalue()
        self.assertTrue(uid in expected_output)

    def test_show_command_with_error_advanced(self):
        """This method helps to test show() command with errors."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(".show()")
        expected_msg = f.getvalue()[:-1]
        self.assertEqual(expected_msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("garbage.show()")
        expected_msg = f.getvalue()[:-1]
        self.assertEqual(expected_msg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.show()")
        expected_msg = f.getvalue()[:-1]
        self.assertEqual(expected_msg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('BaseModel.show("6524359")')
        expected_msg = f.getvalue()[:-1]
        self.assertEqual(expected_msg, "** no instance found **")

    def test_destroy_command(self):
        """This method is used to test destroy for all classes."""
        for class_name in self.classes():
            self.helper_test_for_destroy_command(class_name)
            self.helper_test_for_destroy_command_advanced(class_name)

    def helper_test_for_destroy_command(self, class_name):
        """This method helps to test the destroy command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"create {class_name}")
        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"destroy {class_name} {uid}")
        expected_output = f.getvalue()[:-1]
        self.assertTrue(len(expected_output) == 0)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(".all()")
        self.assertFalse(uid in f.getvalue())

    def test_destroy_command_with_error(self):
        """This method is used to test destroy command with errors."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy")
        expected_msg = f.getvalue()[:-1]
        self.assertEqual(expected_msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy garbage")
        expected_msg = f.getvalue()[:-1]
        self.assertEqual(expected_msg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy BaseModel")
        expected_msg = f.getvalue()[:-1]
        self.assertEqual(expected_msg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy BaseModel 6524359")
        expected_msg = f.getvalue()[:-1]
        self.assertEqual(expected_msg, "** no instance found **")

    def helper_test_for_destroy_command_advanced(self, class_name):
        """This method helps test the destroy command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"create {class_name}")
        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'{class_name}.destroy("{uid}")')
        expected_output = f.getvalue()[:-1]
        self.assertTrue(len(expected_output) == 0)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(".all()")
        self.assertFalse(uid in f.getvalue())

    def test_destroy_command_with_error_advanced(self):
        """This method is used to test destroy() command with errors."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(".destroy()")
        expected_msg = f.getvalue()[:-1]
        self.assertEqual(expected_msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("garbage.destroy()")
        expected_msg = f.getvalue()[:-1]
        self.assertEqual(expected_msg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.destroy()")
        expected_msg = f.getvalue()[:-1]
        self.assertEqual(expected_msg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('BaseModel.destroy("6524359")')
        expected_msg = f.getvalue()[:-1]
        self.assertEqual(expected_msg, "** no instance found **")

    def test_all_command(self):
        """This method is used to test all command for all classes."""
        for class_name in self.classes():
            self.helper_test_for_all_command(class_name)
            self.helper_test_for_all_command_advanced(class_name)

    def helper_test_for_all_command(self, class_name):
        """This method helps to test the all command."""
        uid = self.create_class_for_console_test(class_name)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all")
        expected_output = f.getvalue()[:-1]
        self.assertTrue(len(expected_output) > 0)
        self.assertIn(uid, expected_output)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"all {class_name}")
        expected_output = f.getvalue()[:-1]
        self.assertTrue(len(expected_output) > 0)
        self.assertIn(uid, expected_output)

    def test_all_command_with_error(self):
        """This method is used to test all command with errors."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all garbage")
        expected_msg = f.getvalue()[:-1]
        self.assertEqual(expected_msg, "** class doesn't exist **")

    def helper_test_for_all_command_advanced(self, class_name):
        """This method helps test the .all() command."""
        uid = self.create_class_for_console_test(class_name)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"{class_name}.all()")
        expected_output = f.getvalue()[:-1]
        self.assertTrue(len(expected_output) > 0)
        self.assertIn(uid, expected_output)

    def test_all_command_with_error_advanced(self):
        """This method is used to test all() command with errors."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("garbage.all()")
        expected_msg = f.getvalue()[:-1]
        self.assertEqual(expected_msg, "** class doesn't exist **")

    def test_count_command_for_all(self):
        """This method is used to test count for all classes."""
        for class_name in self.classes():
            self.helper_test_for_count_command_advanced(class_name)

    def helper_test_for_count_command_advanced(self, class_name):
        """This method helps test .count() command."""
        for n in range(20):
            uid = self.create_class_for_console_test(class_name)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"{class_name}.count()")
        expected_output = f.getvalue()[:-1]
        self.assertTrue(len(expected_output) > 0)
        self.assertEqual(expected_output, "20")

    def test_count_command_with_error(self):
        """This method is used to test .count() command with errors."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("garbage.count()")
        expected_msg = f.getvalue()[:-1]
        self.assertEqual(expected_msg, "** class doesn't exist **")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(".count()")
        expected_msg = f.getvalue()[:-1]
        self.assertEqual(expected_msg, "** class name missing **")

    def test_update_command_1(self):
        """This method is used to test update command 1"""
        class_name = "BaseModel"
        attr = "foostr"
        val = "fooval"
        uid = self.create_class_for_console_test(class_name)
        cmd = f'{class_name}.update("{uid}", "{attr}", "{val}")'
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(cmd)
        expected_output = f.getvalue()
        self.assertEqual(len(expected_output), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'{class_name}.show("{uid}")')
        expected_output = f.getvalue()
        self.assertIn(attr, expected_output)
        self.assertIn(val, expected_output)

    def test_update_command_2(self):
        """This method is used to test update command 2"""
        class_name = "User"
        attr = "foostr"
        val = "fooval"
        uid = self.create_class_for_console_test(class_name)
        cmd = f'{class_name}.update("{uid}", "{attr}", "{val}")'
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(cmd)
        expected_output = f.getvalue()
        self.assertEqual(len(expected_output), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'{class_name}.show("{uid}")')
        expected_output = f.getvalue()
        self.assertIn(attr, expected_output)
        self.assertIn(val, expected_output)

    def test_update_command_3(self):
        """This method is used to test update command 3"""
        class_name = "City"
        attr = "foostr"
        val = "fooval"
        uid = self.create_class_for_console_test(class_name)
        cmd = f'{class_name}.update("{uid}", "{attr}", "{val}")'
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(cmd)
        expected_output = f.getvalue()
        self.assertEqual(len(expected_output), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'{class_name}.show("{uid}")')
        expected_output = f.getvalue()
        self.assertIn(attr, expected_output)
        self.assertIn(val, expected_output)

    def test_update_command_4(self):
        """This method is used to test update command 4"""
        class_name = "State"
        attr = "foostr"
        val = "fooval"
        uid = self.create_class_for_console_test(class_name)
        cmd = f'{class_name}.update("{uid}", "{attr}", "{val}")'
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(cmd)
        expected_output = f.getvalue()
        self.assertEqual(len(expected_output), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'{class_name}.show("{uid}")')
        expected_output = f.getvalue()
        self.assertIn(attr, expected_output)
        self.assertIn(val, expected_output)

    def test_update_command_5(self):
        """This method is used to test update command 5"""
        class_name = "Amenity"
        attr = "foostr"
        val = "fooval"
        uid = self.create_class_for_console_test(class_name)
        cmd = f'{class_name}.update("{uid}", "{attr}", "{val}")'
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(cmd)
        expected_output = f.getvalue()
        self.assertEqual(len(expected_output), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'{class_name}.show("{uid}")')
        expected_output = f.getvalue()
        self.assertIn(attr, expected_output)
        self.assertIn(val, expected_output)

    def test_update_command_6(self):
        """This method is used to test update command 6"""
        class_name = "Review"
        attr = "foostr"
        val = "fooval"
        uid = self.create_class_for_console_test(class_name)
        cmd = f'{class_name}.update("{uid}", "{attr}", "{val}")'
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(cmd)
        expected_output = f.getvalue()
        self.assertEqual(len(expected_output), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'{class_name}.show("{uid}")')
        expected_output = f.getvalue()
        self.assertIn(attr, expected_output)
        self.assertIn(val, expected_output)

    def test_update_command_7(self):
        """This method is used to test update command 7"""
        class_name = "Place"
        attr = "foostr"
        val = "fooval"
        uid = self.create_class_for_console_test(class_name)
        cmd = f'{class_name}.update("{uid}", "{attr}", "{val}")'
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(cmd)
        expected_output = f.getvalue()
        self.assertEqual(len(expected_output), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'{class_name}.show("{uid}")')
        expected_output = f.getvalue()
        self.assertIn(attr, expected_output)
        self.assertIn(val, expected_output)

    def test_update_command_for_everything(self):
        """This method is used to test update command for everything."""
        for class_name, cls in self.classes().items():
            uid = self.create_class_for_console_test(class_name)
            for attr, val in self.custom_attr_test.items():
                if type(val) is not str:
                    pass
                match = (type(val) == str)
                self.helper_test_for_update_command(class_name, uid, attr,
                                      val, match, False)
                self.helper_test_for_update_command(class_name, uid, attr,
                                      val, match, True)
            pass
            if class_name == "BaseModel":
                continue
            for attr, attr_type in self.attributes()[class_name].items():
                if attr_type not in (str, int, float):
                    continue
                self.helper_test_for_update_command(class_name, uid, attr,
                                      self.attr_val[attr_type],
                                      True, False)
                self.helper_test_for_update_command(class_name, uid, attr,
                                      self.attr_val[attr_type],
                                      False, True)

    def helper_test_for_update_command(self, class_name, uid, attr, val, quotes, func):
        """This method helps test the update commmand."""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile("file.json"):
            os.remove("file.json")
        uid = self.create_class_for_console_test(class_name)
        value_str = (f'"{val}"' if quotes else f'{val}')
        if func:
            cmd = f'{class_name}.update("{uid}", "{attr}", {value_str})'
        else:
            cmd = f'update {class_name} {uid} {attr} {value_str}'
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(cmd)
        expected_msg = f.getvalue()[:-1]
        self.assertEqual(len(expected_msg), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'{class_name}.show("{uid}")')
        expected_output = f.getvalue()
        self.assertIn(str(val), expected_output)
        self.assertIn(attr, expected_output)

    def test_update_command_with_error(self):
        """This method is used to test the update command with errors."""
        uid = self.create_class_for_console_test("BaseModel")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update")
        expected_msg = f.getvalue()[:-1]
        self.assertEqual(expected_msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update garbage")
        expected_msg = f.getvalue()[:-1]
        self.assertEqual(expected_msg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update BaseModel")
        expected_msg = f.getvalue()[:-1]
        self.assertEqual(expected_msg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update BaseModel 6534276893")
        expected_msg = f.getvalue()[:-1]
        self.assertEqual(expected_msg, "** no instance found **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'update BaseModel {uid}')
        expected_msg = f.getvalue()[:-1]
        self.assertEqual(expected_msg, "** attribute name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'update BaseModel {uid} name')
        expected_msg = f.getvalue()[:-1]
        self.assertEqual(expected_msg, "** value missing **")

    def test_update_command_with_error_advanced(self):
        """This method is used to test update() command with errors."""
        uid = self.create_class_for_console_test("BaseModel")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(".update()")
        expected_msg = f.getvalue()[:-1]
        self.assertEqual(expected_msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("garbage.update()")
        expected_msg = f.getvalue()[:-1]
        self.assertEqual(expected_msg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.update()")
        expected_msg = f.getvalue()[:-1]
        self.assertEqual(expected_msg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.update(6534276893)")
        expected_msg = f.getvalue()[:-1]
        self.assertEqual(expected_msg, "** no instance found **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'BaseModel.update("{uid}")')
        expected_msg = f.getvalue()[:-1]
        self.assertEqual(expected_msg, "** attribute name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'BaseModel.update("{uid}", "name")')
        expected_msg = f.getvalue()[:-1]
        self.assertEqual(expected_msg, "** value missing **")

    def create_class_for_console_test(self, class_name):
        """This method is used to create a class for console tests."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"create {class_name}")
        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)
        return uid

    def help_test_for_dict_equality(self, representation):
        """This method helps to test dictionary equality."""
        regex_pattern = re.compile(r"^\[(.*)\] \((.*)\) (.*)$")
        match_result = regex_pattern.match(representation)
        self.assertIsNotNone(match_result)
        captured_str = match_result.group(3)
        modified_str = re.sub(r"(datetime\.datetime\([^)]*\))", "'\\1'", captured_str)
        parsed_dict = json.loads(modified_str.replace("'", '"'))
        return parsed_dict

    def classes(self):
        """This method is used to return a dictionary of
        valid classes with their references"""

        from models.amenity import Amenity
        from models.base_model import BaseModel
        from models.city import City
        from models.place import Place
        from models.review import Review
        from models.state import State
        from models.user import User

        classes = {"BaseModel": BaseModel,
                   "Amenity": Amenity,
                   "City": City,
                   "Place": Place,
                   "Review": Review,
                   "State": State,
                   "User": User}
        return classes

    def attributes(self):
        """This method is used to return attributes with
        their types for classname"""

        attributes = {
            "Amenity":
                     {"name": str},
            "BaseModel":
                     {"id": str,
                      "created_at": datetime.datetime,
                      "updated_at": datetime.datetime},
            "City":
                     {"state_id": str,
                      "name": str},
            "Place":
                     {"city_id": str,
                      "user_id": str,
                      "name": str,
                      "description": str,
                      "number_rooms": int,
                      "number_bathrooms": int,
                      "max_guest": int,
                      "price_by_night": int,
                      "latitude": float,
                      "longitude": float,
                      "amenity_ids": list},
            "Review":
                     {"place_id": str,
                      "user_id": str,
                      "text": str},
            "State":
                     {"name": str},
            "User":
                     {"email": str,
                      "password": str,
                      "first_name": str,
                      "last_name": str}
        }
        return attributes


if __name__ == "__main__":
    unittest.main()
