#!/usr/bin/python3
"""
Unittest class for base_model
"""

import os
import unittest
import models
from models import base_model
from models.base_model import BaseModel
from models.user import User
from models import storage
from datetime import datetime
from io import StringIO
import json
import sys


class TestFileStorage(unittest.TestCase):
    """All test cases of BaseModel class"""
    @classmethod
    def setUpClass(self):
        stor_path = "file.json"
        """Preserve existing test file.json
        if any"""
        try:
            os.rename(stor_path, "your_json")
        except Exception:
            pass

    @classmethod
    def tearDownClass(self):
        """Delete unit test json and restore previous
        Reset __objects"""
        stor_path = "file.json"
        if os.path.exists(stor_path):
            os.remove(stor_path)

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
        """testing addition of a new object to the storage"""
        obj2 = BaseModel()
        all_objs = storage.all()
        key = f"BaseModel.{obj2.id}"
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

    def test_reload_empty_json(self):
        """test for trying to reload storage when no json file"""
        self.assertIsNone(storage.reload())

    def test_child_new(self):
        """Test new using subclass"""
        """all_objs = storage.all()
        key = f"BaseModel.{obj2.id}"
        self.assertTrue(key in all_objs)"""
        us = User()
        # storage.new(us)
        self.assertIn("User." + us.id, storage.all().keys())
        self.assertIn(us, storage.all().values())

    def test_child_save(self):
        """Test save using subclass"""
        us = User()
        storage.new(us)
        storage.save()
        save_text = ""
        with open("file.json", "r") as f:
            save_text = f.read()
            self.assertIn("User." + us.id, save_text)



if __name__ == '__main__':
    unittest.main()
