#!/usr/bin/python3
"""
Unittest class for base_model
"""

import os
import unittest
from models.base_model import BaseModel
from models.user import User
from datetime import datetime
from io import StringIO
import sys
from models import storage
import json


class TestUser(unittest.TestCase):
    """All test cases of User class"""
    @classmethod
    def setUpClass(cls):
        """removing file.json to start from empty"""
        stor_path = "file.json"
        with open(stor_path, "w") as f:
            f.write("{}")
        storage.reload()
        if os.path.exists(stor_path):
            os.remove(stor_path)

    @classmethod
    def tearDownClass(cls):
        """removing file.json that has been created
        and manipulated in these tests"""
        stor_path = "file.json"
        if os.path.exists(stor_path):
            os.remove(stor_path)

    def setUp(self):
        """creating a User before each test case"""
        self.obj = User()

    def tearDown(self):
        """Instructions to do after each test"""
        stor_path = "file.json"
        with open(stor_path, "w") as f:
            f.write("{}")
        storage.reload()
        if os.path.exists(stor_path):
            os.remove(stor_path)

    def test_user_parent(self):
        """Checking that User is a subclass of BaseModel"""
        self.assertTrue(
            self.obj.__class__ in BaseModel.__subclasses__())

    def test_user_attr_types(self):
        """checking the attribute types"""
        list_attr = [self.obj.email, self.obj.password, self.obj.id,
                     self.obj.first_name, self.obj.last_name,
                     self.obj.created_at, self.obj.updated_at]
        output_types = [type(attr) for attr in list_attr]
        expected_types = [str] * 5 + [datetime] * 2
        self.assertEqual(output_types, expected_types)

    def test_storage_new(self):
        """testing addition of a new object to the storage"""
        obj2 = User()
        all_objs = storage.all()
        key = f"User.{obj2.id}"
        self.assertTrue(key in all_objs)

    def test_storage_save_reload(self):
        """testing save and reload methods"""
        storage.save()
        self.assertTrue(os.path.isfile("file.json"))
        all_objs = storage.all()
        expected = {k: v.to_dict() for k, v in all_objs.items()}
        with open("file.json") as f:
            output = json.load(f)
        self.maxDiff = None
        self.assertEqual(output, expected)


if __name__ == '__main__':
    unittest.main()
