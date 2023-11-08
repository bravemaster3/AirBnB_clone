#!/usr/bin/python3
"""
This program is the entry point of the command interpreter
"""


import cmd
import json
import models
from models.base_model import BaseModel
import re
# from models.engine import file_storage


class HBNBCommand(cmd.Cmd):
    """definition of the CLI class"""
    prompt = "(hbnb) "

    def fetch_class(self, name):
        """returns a class given its name as string"""
        if name in [cls.__name__ for cls in [BaseModel] +
                    BaseModel.__subclasses__()]:
            my_class = [cls for cls in [BaseModel] +
                        BaseModel.__subclasses__()
                        if name == cls.__name__][0]
            return my_class
        else:
            return False

    def handle_errors(self, line, crud="RD"):
        """generic error handler"""
        if line == "":
            print("** class name missing **")
            return -1
        else:
            tokens = self.magic_splitter(line)
            if self.fetch_class(tokens[0]) is False:
                print("** class doesn't exist **")
                return -1
            elif crud == "RD" or crud == "U":
                if len(tokens) == 1:
                    print("** instance id missing **")
                    return -1
                if len(tokens) > 1:
                    mod_id = f"{tokens[0]}.{tokens[1]}"
                    if mod_id not in models.storage.all():
                        print("** no instance found **")
                        return -1
                if crud == "U":
                    if len(tokens) == 2:
                        print("** attribute name missing **")
                        return -1
                    if len(tokens) == 3:
                        print("** value missing **")
                        return -1

    def magic_splitter(self, string):
        """splits a string without splitting double quote content"""
        result = re.findall(r'[^"\s]+|"[^"]*"', string)
        result = [
            x.strip('"') if x.startswith('"') and x.endswith('"') else x
            for x in result
        ]
        return result

    def do_create(self, line):
        """Creates a new instance of Basemodel, saves it to the JSON file,
        and prints the id. Eg: create BaseModel
        """
        err = self.handle_errors(line, crud="C")
        tokens = self.magic_splitter(line)
        if err != -1 and self.fetch_class(tokens[0]) is not False:
            my_class = self.fetch_class(tokens[0])
            my_obj = my_class()
            print(my_obj.id)
            my_obj.save()

    def do_show(self, line):
        """Prints the string representation of an instance based on
        the class name and id. Ex: $ show BaseModel 1234-1234-1234
        """
        err = self.handle_errors(line, crud="RD")
        if err != -1:
            tokens = self.magic_splitter(line)
            print(models.storage.all()[f"{tokens[0]}.{tokens[1]}"])

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id,
        save the change into the JSON file.
        Ex: $ destroy BaseModel 1234-1234-1234
        """
        err = self.handle_errors(line, crud="RD")
        if err != -1:
            tokens = self.magic_splitter(line)
            del models.storage.all()[f"{tokens[0]}.{tokens[1]}"]
            models.storage.save()

    def do_all(self, line, print_out=True, return_out=False):
        """Prints all string representation of all instances based
        or not on the class name. Ex: $ all BaseModel or $ all
        """
        tokens = self.magic_splitter(line)
        if not tokens:
            print([obj.__str__() for k, obj in models.storage.all().items()])
        elif self.fetch_class(tokens[0]) is not False:
            ret = [obj.__str__() for k, obj in models.storage.all().items() if
                   obj.__class__.__name__ == tokens[0]]
            if print_out:
                print(ret)
            if return_out:
                return ret
        else:
            print("** class doesn't exist **")

    def do_update(self, line):
        """Updates an instance based on the class name and id by adding
        or updating attribute (save the change into the JSON file).
        Ex: $ update BaseModel 1234-1234-1234 email "aibnb@mail.com"
        """
        err = self.handle_errors(line, crud="U")
        if err != -1:
            tokens = self.magic_splitter(line)
            mod_id = f"{tokens[0]}.{tokens[1]}"
            var_type = None
            if hasattr(models.storage.all()[mod_id], tokens[2]):
                var_type = type(getattr(
                    models.storage.all()[mod_id], tokens[2]))

            if not var_type:
                setattr(models.storage.all()[mod_id],
                        tokens[2], tokens[3])
            else:
                setattr(models.storage.all()[mod_id],
                        tokens[2], var_type(tokens[3]))
            models.storage.save()

    def default(self, line: str) -> None:
        """"Overrides the default behaviour of the cmd line for unknown cmd
        """
        token = self.magic_splitter(line)
        toks = token[0].split(".")
        cls_list = [BaseModel] + BaseModel.__subclasses__()
        cls_names = [cls.__name__ for cls in cls_list]
        met_list1 = ["all()", "count()"]
        if len(toks) == 2:
            command = toks[1].split("(")[0]
            arg = toks[1].split("(")[1].split(")")[0]
        if len(toks) == 2 and toks[0] in cls_names and toks[1] in met_list1:
            all_obj = self.do_all(
                toks[0], print_out=False, return_out=True)
            if toks[1] == "all()":
                print('[' + ', '.join(all_obj) + ']')
            if toks[1] == "count()":
                print(len(all_obj))
        elif len(toks) == 2 and toks[0] in cls_names and command == "show":
            self.do_show(f"{toks[0]} {arg}")
        elif len(toks) == 2 and toks[0] in cls_names and command == "destroy":
            self.do_destroy(f"{toks[0]} {arg}")
        elif len(toks) == 2 and toks[0] in cls_names and command == "update":
            arg = line.split(")")[0].split("(")[1]
            """FAILED ATTEMPT TO DO TASK 16... COMBINED WITH 15.
            spl = arg.split(", ")
            if len(spl) >= 2 and type(json.loads(spl[1])) is dict:
                print(spl)
                for name, value in json.loads(spl[1]).items():
                    self.do_update(f"{toks[0]} {name} {value}")
            else:
                self.do_update(f"{toks[0]} {arg.replace(',', '')}")
            """
            self.do_update(f"{toks[0]} {arg.replace(',', '')}")
        else:
            return super().default(line)

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
