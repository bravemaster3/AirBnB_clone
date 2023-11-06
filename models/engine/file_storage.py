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
        self.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj.to_dict()

    def save(self):
        """"serializes and saves __objects"""
        with open(self.__file_path, "w") as f:
            json.dump(self.__objects, f)

    def reload(self):
        """deserializes a json file"""
        if os.path.isfile(self.__file_path):
            with open(self.__file_path) as f:
                self.__objects = json.load(f)
