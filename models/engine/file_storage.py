#!/usr/bin/python3
"""
This module contains a class for file storage
"""

import json
import os
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage:
    """Definition of the class FileStorage"""
    __file_path: str = "file.json"
    __objects: dict = {}

    def all(self):
        """returns all objects"""
        return self.__objects

    def new(self, obj):
        """sets new object in dictionnary of objects"""
        self.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj

    def save(self):
        """"serializes and saves __objects"""
        with open(self.__file_path, "w") as f:
            json.dump({k: v.to_dict() for k, v in self.__objects.items()}, f)

    def all_classes(self, cls):
        """Return a dictionary of parent class and all dirrect subclasses"""
        classes = set([cls]).union(cls.__subclasses__())
        return {c.__name__: c for c in classes}

    def reload(self):
        """deserializes a json file"""
        my_classes = self.all_classes(BaseModel)
        if os.path.isfile(self.__file_path):
            with open(self.__file_path, "r") as f:
                my_objs = json.load(f)
                self.__objects = {k: my_classes[v['__class__']](**v)
                                  for k, v in my_objs.items()
                                  if v['__class__'] in my_classes}
