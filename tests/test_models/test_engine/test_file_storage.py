#!/usr/bin/python3
"""Defines unittests for models/engine/file_storage.py.

Unittest classes:
    TestFileStorage_instantiation
    TestFileStorage_methods
"""
import os
import json
import models
import unittest
from datetime import datetime
from models.base_model import BaseModel
# from models import storage
from models.engine import file_storage
from models.user import User


class TestFileStorage_methods(unittest.TestCase):
    """Unittests for testing methods of the FileStorage class."""

    @classmethod
    def setUp(self):
        """Rename existing file.json"""
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        """Remove unittest file.json and restore
        previous"""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

        file_storage.FileStorage._FileStorage__objects = {}

    def setUp(self):
        """creating a BaseModel before each test case"""
        self.obj = BaseModel()

    def tearDown(self):
        """Instructions to do after each test"""
        stor_path = "file.json"
        with open(stor_path, "w") as f:
            f.write("{}")
        storage.reload()
        if os.path.exists(stor_path):
            os.remove(stor_path)

    def test_attr_types(self):
        """testing the type of Filestorage private attributes"""
        all_objs = storage.all()
        self.assertIsNotNone(all_objs)
        my_dict = {
            f'{self.obj.__class__.__name__}.{self.obj.id}': self.obj}
        self.maxDiff = None
        self.assertEqual(my_dict, all_objs)

    def test_storage_new(self):
        """testing addition of a new object to the storage
        In parent and subclass"""
        obj2 = BaseModel()
        obj3 = User()
        all_objs = storage.all()
        key2 = f"BaseModel.{obj2.id}"
        key3 = f"User.{obj3.id}"
        with self.subTest():
            self.assertTrue((key2, obj2) in all_objs.items())
        with self.subTest():
            self.assertTrue((key3, obj3) in all_objs.items())

    def test_storage_save_reload(self):
        """testing save and reload methods
        in parent and subclass"""
        obj2 = User()
        storage.save()
        self.assertTrue(os.path.isfile("file.json"))
        all_objs = storage.all()
        expected = {k: v.to_dict() for k, v in all_objs.items()}
        with open("file.json") as f:
            output = json.load(f)
        self.maxDiff = None
        self.assertEqual(output, expected)

    def test_reload_empty_json(self):
        """test for trying to reload storage when no json file"""
        self.assertIsNone(storage.reload())


if __name__ == '__main__':
    unittest.main()
