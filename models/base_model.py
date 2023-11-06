#!/usr/bin/python3
"""
This module defines the base class for all other models
in the airbnb project
"""

from datetime import datetime
import uuid
from models import storage


class BaseModel:
    """Definition of BaseModel class"""

    def __init__(self, *args, **kwargs):
        """Instanciation method"""
        if kwargs:
            for key, value in kwargs.items():
                if key in ["created_at", "updated_at"]:
                    setattr(self, key, datetime.fromisoformat(value))
                elif key != "__class__":
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            storage.new(self)

    def __str__(self):
        """prints a formatted representation of the object"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """saves updates to a class"""
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """returns a dictionary representation of the object"""
        # print("TESTTTTT", self.__dict__)
        my_dict = self.__dict__.copy()
        my_dict["__class__"] = self.__class__.__name__
        my_dict["created_at"] = my_dict["created_at"].isoformat()
        my_dict["updated_at"] = my_dict["updated_at"].isoformat()
        # print("TESTTTTTTT", my_dict)
        return my_dict
