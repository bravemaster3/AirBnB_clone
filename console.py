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
# from models.engine import file_storage
# ^(\"[^\"]*\")(?:, (.*))?$ matches attr and dict
# ^({.*})$ dictionary only


class HBNBCommand(cmd.Cmd):
    """definition of the CLI class"""
    prompt = "(hbnb) "


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
        elif argc >=3 and len(args) == 2:
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
                all_objects = [obj for obj in all_objects if obj.__class__.__name__ == tokens[0]]
            if count:
                return len(all_objects)
            print([obj.__str__() for obj in all_objects])



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
            cast_attr_value = self.cast_attr(tokens[3], attr_type)
            setattr(instance, tokens[2], cast_attr_value)
            storage.save()

    def cast_attr(self, attr_value, _type=None):
        """Cast value to desired type"""

        if _type is not None:
            try:
                _type(attr_value)
                return _type(attr_value)
            except:
                if _type == int:
                    try:
                        _type(float(attr_value))
                        return _type(float(attr_value))
                    except:
                        pass
        try:
            if "." in attr_value:
                float(attr_value)
                return float(attr_value)
            int(attr_value)
            return int(attr_value)
        except:
            pass
        return attr_value

    def map_method(self, name, line):
        """find methods currently in class"""        
        my_method = getattr(self, name, None)
        if callable(my_method):
            my_method(line)

    def default(self, line: str) -> None:
        """Override the default"""
        """Still a working progress"""
        match = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\)?)$", line)

        if match:
            my_dict = None
            class_name, method_name, args = match.groups()
            method_name = method_name if method_name == "count" else "do_" + method_name

            dict_matched = re.search(r'^(\"[^\"]*\"), ({.*})$', args)
            if dict_matched:
                instance_id, my_dict_str = dict_matched.groups()
                my_dict = literal_eval(my_dict_str)
                if isinstance(my_dict, dict):
                    # print(my_dict)
                    my_dict_str = my_dict_str.strip("{}")
                    dict_str_list = [item for substring in my_dict_str.split(",") for item in substring.split(":")]
                    i = 0
                    for  j in range(1, len(dict_str_list), 2):
                        new_line = " ".join([class_name, instance_id, dict_str_list[i] , dict_str_list[j]])
                        self.map_method(method_name, new_line)
                        i += 2

            else:
                args = args.replace("'", " ").split(",")
                arg_line = " ".join(args)
                new_line = " ". join([class_name, arg_line])
                self.map_method(method_name, new_line)

        else:
            return super().default(line)

    def count(self, line):
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
