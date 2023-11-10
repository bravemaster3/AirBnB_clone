#!/usr/bin/python3
"""
This program is the entry point of the command interpreter
"""


import cmd
from models import storage
from models.base_model import BaseModel
import re
import shlex
from ast import literal_eval


class HBNBCommand(cmd.Cmd):
    """definition of the CLI class"""
    prompt = "(hbnb) "
    __from_match = False

    def fetch_class(self, name):
        """returns a class given its name as string"""
        return storage.all_classes(BaseModel).get(name)

    def my_handler(self, line, argc=1, all=False):
        """Splits line into arguments
        Runs checks on the arguments
        Returns tuple of error flag and list of arguments"""
        args = self.magic_splitter(line)
        err = False
        if not args and not all:
            print("** class name missing **")
            err = True
        elif args and not self.fetch_class(args[0]):
            print("** class doesn't exist **")
            err = True
        elif argc >= 2 and len(args) == 1:
            print("** instance id missing **")
            err = True
        elif argc >= 2 and not storage.all().get(f"{args[0]}.{args[1]}"):
            print("** no instance found **")
            err = True
        elif argc >= 3 and len(args) == 2:
            print("** attribute name missing **")
            err = True
        elif argc > 3 and len(args) == 3:
            print("** value missing **")
            err = True
        return err, args

    def magic_splitter(self, string):
        """splits a string without splitting double quote content"""
        return shlex.split(string)

    def do_create(self, line):
        """Creates a new instance of Basemodel, saves it to the JSON file,
        and prints the id. Eg: create BaseModel
        """
        err, tokens = self.my_handler(line)
        if not err and self.fetch_class(tokens[0]):
            my_class = self.fetch_class(tokens[0])
            my_object = my_class()
            print(my_object.id)
            my_object.save()

    def do_show(self, line):
        """Prints the string representation of an instance based on
        the class name and id. Ex: $ show BaseModel 1234-1234-1234
        """
        err, tokens = self.my_handler(line, 2)
        if not err:
            print(storage.all().get(f"{tokens[0]}.{tokens[1]}"))

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id,
        save the change into the JSON file.
        Ex: $ destroy BaseModel 1234-1234-1234
        """
        err, tokens = self.my_handler(line, 2)
        if not err:
            del storage.all()[f"{tokens[0]}.{tokens[1]}"]
            storage.save()

    def do_all(self, line, count=False):
        """Prints all string representation of all instances based
        or not on the class name. Ex: $ all BaseModel or $ all
        """
        err, tokens = self.my_handler(line, all=True)
        if not err:
            all_objects = [obj for k, obj in storage.all().items()]
            if tokens:
                all_objects = [obj for obj in all_objects
                               if obj.__class__.__name__ == tokens[0]]
            if count:
                return len(all_objects)

            ret_obj_str = [obj.__str__() for obj in all_objects]
            if self.__from_match:
                print("[" + ", ".join(ret_obj_str) + "]")
            else:
                print(ret_obj_str)

    def do_update(self, line):
        """Updates an instance based on the class name and id by adding
        or updating attribute (save the change into the JSON file).
        Ex: $ update BaseModel 1234-1234-1234 email "aibnb@mail.com"
        """
        err, tokens = self.my_handler(line, 4)
        if not err:
            instance_id = f"{tokens[0]}.{tokens[1]}"
            instance = storage.all().get(instance_id)
            attr_value = getattr(instance, tokens[2], None)
            attr_type = type(attr_value) if attr_value is not None else None

            if attr_type:
                new_value = attr_type(tokens[3])
            else:
                new_value = self.cast_attr(tokens[3])
            setattr(instance, tokens[2], new_value)
            storage.save()

    def cast_attr(self, value, data_type=None):
        """Cast value to exisiting data type or
        cast to appropriate data type"""
        try:
            if data_type is not None:
                return data_type(value)
            elif "." in value:
                return float(value)
            else:
                return int(value)
        except (ValueError, TypeError) as e:
            if data_type and data_type == int:
                try:
                    return data_type(float(value))
                except:
                    pass
            elif not data_type:
                return value
            else:
                pass

    def default(self, line: str) -> None:
        """Override the default"""
        allowed_methods = ["all", "count", "destroy", "show", "update"]
        match = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\)?).*$", line)

        if match:
            class_name, method_name, args = match.groups()

        if match and method_name in allowed_methods:
            dict_matched = re.search(r'^(\"[^\"]*\"), ({.*})$', args)

            if dict_matched:
                instance_id, dict_str = dict_matched.groups()

                if isinstance(literal_eval(dict_str), dict):
                    dict_str = dict_str.strip("{}")
                    dict_list = [item for substring in dict_str.split(",")
                                 for item in substring.split(":")]
                    for j in range(0, len(dict_list), 2):
                        new_line = " ".join([method_name, class_name,
                                             instance_id, dict_list[j],
                                             dict_list[j+1]])
                        self._exec_cmd(new_line)
            else:
                # arg_line = " ".join(args.split(","))
                arg_line = " ".join(args.replace("'", " ").split(","))
                cmd_args = " ". join([class_name, arg_line])
                if method_name == "count":
                    self.count(cmd_args)
                else:
                    new_line = " ".join([method_name, cmd_args])
                    self._exec_cmd(new_line)
        else:
            return super().default(line)

    def _exec_cmd(self, line):
        """Execute commands"""
        self.__from_match = True
        self.onecmd(line)
        self.__from_match = False

    def count(self, line):
        """Return number of instances"""
        print(self.do_all(line, True))

    def emptyline(self):
        """Defines what happens when no command is issued
        """
        pass

    def do_quit(self, line):
        """Quit command to exit the program
        """
        return True

    def do_EOF(self, line):
        """EOF command / CTRL+D to exit the program
        """
        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
