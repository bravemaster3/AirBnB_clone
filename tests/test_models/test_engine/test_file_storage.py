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
from models.engine.file_storage import FileStorage
from models.user import User


class TestFileStorage_methods(unittest.TestCase):
    """Unittests for testing methods of the FileStorage class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}
    
    def test_new(self):
        """Yes"""            
        us = User()
        models.storage.new(us)
        self.assertIn("User." + us.id, models.storage.all().keys())
        self.assertIn(us, models.storage.all().values())

    def test_save(self):
        us = User()
        models.storage.save()
        save_text = ""
        with open("file.json", "r") as f:
            save_text = f.read()
            self.assertIn("User." + us.id, save_text)


if __name__ == "__main__":
    unittest.main()
