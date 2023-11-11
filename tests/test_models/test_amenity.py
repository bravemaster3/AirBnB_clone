#!/usr/bin/python3
"""
Unittest class for base_model
"""

import os
import unittest
from models.base_model import BaseModel
from models.amenity import Amenity
from datetime import datetime
from io import StringIO
import sys
from models import storage
import json


class TestAmenity(unittest.TestCase):
    """All test cases of Amenity class"""
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
        """creating a Amenity before each test case"""
        self.obj = Amenity()

    def tearDown(self):
        """Instructions to do after each test"""
        stor_path = "file.json"
        with open(stor_path, "w") as f:
            f.write("{}")
        storage.reload()
        if os.path.exists(stor_path):
            os.remove(stor_path)

    def test_Amenity_parent(self):
        """Checking that Amenity is a subclass of BaseModel"""
        self.assertTrue(
            self.obj.__class__ in BaseModel.__subclasses__())

    def test_Amenity_attr_types(self):
        """checking the attribute types"""
        list_attr = [self.obj.name, self.obj.id,
                     self.obj.created_at, self.obj.updated_at]
        output_types = [type(attr) for attr in list_attr]
        expected_types = [str] * 2 + [datetime] * 2
        self.assertEqual(output_types, expected_types)

    def test_storage_new(self):
        """testing addition of a new object to the storage"""
        obj2 = Amenity()
        all_objs = storage.all()
        key = f"Amenity.{obj2.id}"
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
