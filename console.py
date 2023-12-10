#!/usr/bin/python3
"""This is a module with a class called HBNBCommand 
used for the command interpreter or the console."""

import cmd
import json
import re
from models.base_model import BaseModel
from models import storage


class HBNBCommand(cmd.Cmd):

    """This is a class that inherits from the Cmd class within
    the cmd module used for the command interpreter."""

    prompt = "(hbnb) "

    def default(self, line):
        """This is a method called default which is used to catch
        commands if nothing else matches"""
        self._precmd(line)

    def do_quit(self, line):
        """This method is a Quit command to exit the program.
        """
        return True

    def do_EOF(self, line):
        """This method is used to handle the End Of File."""
        print()
        return True

    def emptyline(self):
        """This method doesn't do anything while
        pressing ENTER."""
        pass

    def _precmd(self, line):
        """Hook command interpreted just before the command line
        'line' is interpreted."""

        match_pattern = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", line)
        if not match_pattern:
            return line

        class_name = match_pattern.group(1)
        Method = match_pattern.group(2)
        args = match_pattern.group(3)
        args_and_uid_match = re.search('^"([^"]*)"(?:, (.*))?$', args)

        if args_and_uid_match:
            uid = args_and_uid_match.group(1)
            dict_or_attr = args_and_uid_match.group(2)
        else:
            uid = args
            dict_or_attr = False

        attr_and_value = ""

        if dict_or_attr and Method == "update":
            dict_match = re.search('^({.*})$', dict_or_attr)
            if dict_match:
                self.update_dict(class_name, uid, dict_match.group(1))
                return ""

            attr_and_value_match = re.search(
                '^(?:"([^"]*)")?(?:, (.*))?$', dict_or_attr)
            if attr_and_value_match:
                attr_and_value = (attr_and_value_match.group(
                    1) or "") + " " + (attr_and_value_match.group(2) or "")

        cmd = Method + " " + class_name + " " + uid + " " + attr_and_value
        self.onecmd(cmd)
        return cmd

    def update_dict(self, class_name, uid, str_dict):
        """This is a helper method for the update method
        with a dictionary."""

        my_dict = json.loads(str_dict.replace("'", '"'))
        if not class_name:
            print("** class name missing **")
        elif class_name not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            key = f"{class_name}.{uid}"

            if key not in storage.all():
                print("** no instance found **")
            else:
                attributes = storage.attributes()[class_name]

                for attr, value in my_dict.items():
                    if attr in attributes:
                        value = attributes[attr](value)
                    setattr(storage.all()[key], attr, value)
                storage.all()[key].save()


    def do_all(self, line):
        """This method is used for printing all the string
        representation of every instance."""

        if line != "":
            args = line.split(' ')
            if args[0] not in storage.classes():
                print("** class doesn't exist **")
            else:
                my_list = [str(obj) for key, obj in storage.all().items()
                      if type(obj).__name__ == args[0]]
                print(my_list)
        else:
            my_list = [str(obj) for key, obj in storage.all().items()]
            print(my_list)

    def do_count(self, line):
        """This method is used for counting the
        instances of a class."""

        args = line.split(' ')

        if not args[0]:
            print("** class name missing **")
        elif args[0] not in storage.classes():
            print("** class doesn't exist **")
        else:
            count = len([
                n for n in storage.all() if n.startswith(
                    args[0] + '.')])
            print(count)

    def do_create(self, line):
        """This method is used to create a new instance of BaseModel,
        saves it(to the JSON file) and prints the id."""

        if line is None or line == "":
            print("** class name missing **")
        elif line not in storage.classes():
            print("** class doesn't exist **")
        else:
            result = storage.classes()[line]()
            result.save()
            print(result.id)

    def do_destroy(self, line):
        """This method is used for deleting an instance
        by the use of id and class name."""

        if line is None or line == "":
            print("** class name missing **")
        else:
            args = line.split(' ')

            if args[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(args) < 2:
                print("** instance id missing **")
            else:
                key = f"{args[0]}.{args[1]}"

                if key not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[key]
                    storage.save()

    def do_show(self, line):
        """This method is used for the purpose of printing
        the string representation of an instance."""

        if line is None or line == "":
            print("** class name missing **")

        else:
            args = line.split(' ')
            if args[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(args) < 2:
                print("** instance id missing **")
            else:
                key = f"{args[0]}.{args[1]}"
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    print(storage.all()[key])

    def do_update(self, line):
        """This method is used for updating an instance
        through updation or addition of an attribute."""

        if line is None or line == "":
            print("** class name missing **")
            return

        rex = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        match_pattern = re.search(rex, line)
        class_name = match_pattern.group(1)
        uid = match_pattern.group(2)
        attr = match_pattern.group(3)
        val = match_pattern.group(4)

        if not match_pattern:
            print("** class name missing **")
        elif uid is None:
            print("** instance id missing **")
        elif class_name not in storage.classes():
            print("** class doesn't exist **")
        else:
            key = f"{class_name}.{uid}"

            if key not in storage.all():
                print("** no instance found **")
            elif not val:
                print("** value missing **")
            elif not attr:
                print("** attribute name missing **")
            else:
                type_cast = None
                match = re.search('^".*"$', val)

                if not match:
                    if '.' in val:
                        type_cast = float
                    else:
                        type_cast = int
                else:
                    val = val.replace('"', '')

                attributes = storage.attributes()[class_name]
                if attr in attributes:
                    val = attributes[attr](val)
                elif type_cast:
                    try:
                        val = type_cast(val)
                    except ValueError:
                        pass

                setattr(storage.all()[key], attr, val)
                storage.all()[key].save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
