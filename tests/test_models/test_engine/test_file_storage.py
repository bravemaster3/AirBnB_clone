#!/usr/bin/python3
"""
Unittest class for base_model
"""

import os
import unittest
from models import base_model
from models.base_model import BaseModel
from models.user import User
from models.engine import file_storage
from models import storage
from datetime import datetime
from io import StringIO
import json
import sys


class TestFileStorage(unittest.TestCase):
    """All test cases of BaseModel class"""
    @classmethod
    def setUpClass(cls):
        """removing file.json to start from empty"""
        # reload(base_model)
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
    
    class TestFileStorage_methods(unittest.TestCase):
        """additional tests for save, reload and objects"""
        @classmethod
        def setUp(self):
            try:
                os.rename("file.json", "my_file")
            except IOError:
                pass
        @classmethod
        def tearDown(self) -> None:
            try:
                os.remove("file.json")
            except IOError:
                pass
            try:
                os.rename("tmp", "file.json")
            except IOError:
                pass
            file_storage.FileStorage._FileStorage__objects = {}
        
        def test_new(self):
            """Test the .new() method"""
            my_bm = BaseModel()
            my_us = User()
            storage.new(my_bm)
            storage.new(my_us)
            self.assertIn("BaseModel." + my_bm.id, storage.all().keys())
            self.assertIn(my_bm, storage.all().values())
            self.assertIn("User." + my_us.id, storage.all().keys())
            self.assertIn(my_us, storage.all().values())

        def test_save(self):
            """Test the .save() method"""
            my_bm = BaseModel()
            my_us = User()
            storage.new(my_bm)
            storage.new(my_us)
            storage.save()
            save_text = ""
            with open("file.json", "r") as f:
                save_text = f.read()
                self.assertIn("BaseModel." + my_bm.id, save_text)
                self.assertIn("User." + my_us.id, save_text)



if __name__ == '__main__':
    unittest.main()
