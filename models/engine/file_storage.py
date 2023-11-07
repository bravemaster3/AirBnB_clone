#!/usr/bin/python3
"""
This module contains a class for file storage
"""

import json
import os



class FileStorage:
    """Definition of the class FileStorage"""
    __file_path = "file.json"
    __objects = {}

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

    def reload(self):
        """deserializes a json file"""
        if os.path.isfile(self.__file_path):
            with open(self.__file_path, "r") as f:
                my_objs = json.load(f)
                from models.base_model import BaseModel
                self.__objects = {k: BaseModel(**v)
                                  for k, v in my_objs.items()}
