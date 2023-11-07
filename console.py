#!/usr/bin/python3
"""
This program is the entry point of the command interpreter
"""


import cmd
import models
from models.base_model import BaseModel
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

    def handle_errors(self, line, create=False):
        """generic error handler"""
        if line == "":
            print("** class name missing **")
            return -1
        else:
            tokens = line.split()
            if self.fetch_class(tokens[0]) is False:
                print("** class doesn't exist **")
                return -1
            elif create is False:
                if len(tokens) == 1:
                    print("** instance id missing **")
                    return -1
                if len(tokens) > 1:
                    mod_id = f"{tokens[0]}.{tokens[1]}"
                    if mod_id not in models.storage.all():
                        print("** no instance found **")
                        return -1

    def do_create(self, line):
        """Creates a new instance of Basemodel, saves it to the JSON file,
        and prints the id. Eg: create BaseModel
        """
        err = self.handle_errors(line, create=True)
        tokens = line.split()
        if err != -1 and self.fetch_class(tokens[0]) is not False:
            my_class = self.fetch_class(tokens[0])
            my_obj = my_class()
            print(my_obj.id)
            my_obj.save()

    def do_show(self, line):
        """Prints the string representation of an instance based on
        the class name and id. Ex: $ show BaseModel 1234-1234-1234
        """
        err = self.handle_errors(line)
        if err != -1:
            tokens = line.split()
            print(models.storage.all()[f"{tokens[0]}.{tokens[1]}"])

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id,
        save the change into the JSON file.
        Ex: $ destroy BaseModel 1234-1234-1234
        """
        err = self.handle_errors(line)
        if err != -1:
            tokens = line.split()
            del models.storage.all()[f"{tokens[0]}.{tokens[1]}"]
            models.storage.save()

    def do_all(self, line):
        """Prints all string representation of all instances based
        or not on the class name. Ex: $ all BaseModel or $ all
        """
        tokens = line.split()
        if not tokens:
            print([obj.__str__() for k, obj in models.storage.all().items()])
        elif self.fetch_class(tokens[0]) is not False:
            print([obj.__str__() for k, obj in models.storage.all().items() if
                   obj.__class__.__name__ == tokens[0]])
        else:
            print("** class doesn't exist **")

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
