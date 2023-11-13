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


class TestBaseModel(unittest.TestCase):
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

    def stdout_capturer(self, method_to_run, *args, **kwargs):
        """method for capturing stdout"""
        captured_output = StringIO()
        sys.stdout = captured_output
        method_to_run(*args, **kwargs)
        sys.stdout = sys.__stdout__
        return captured_output.getvalue()

    def test_default_attr_types(self):
        """testing that the auto id is a string"""
        self.assertIs(type(self.obj.id), str)
        self.assertIs(type(self.obj.created_at), datetime)
        self.assertIs(type(self.obj.updated_at), datetime)

    def test_setting_attr(self):
        """testing setting new attributes, any kind"""
        self.obj.name = "My First Model"
        self.obj.my_number = 89
        self.obj.none_var = None
        subset = {'fruit': 'banana', 'number': 1}
        self.obj.a_dict = subset
        self.assertTrue(set({'a_dict': subset}).issubset(
            set(self.obj.__dict__)))
        self.assertIsNone(self.obj.none_var)

    def test_str_print(self):
        """testing the return of str"""
        output = self.obj.__str__()
        expected = f"[BaseModel] ({self.obj.id}) {self.obj.__dict__}"
        self.assertEqual(output, expected)
        self.obj.name = "My First Model"
        self.obj.my_number = 89
        """"checking that the actually printing is ok"""
        stdout = self.stdout_capturer(print, self.obj)
        expected = f"[BaseModel] ({self.obj.id}) {self.obj.__dict__}\n"
        self.assertEqual(stdout, expected)

    def test_created_updated_time(self):
        """testing that created and updated times are same at start"""
        self.assertEqual(self.obj.created_at, self.obj.updated_at)

    def test_save_updated_time(self):
        """tests that updating changes the datetime"""
        self.assertEqual(self.obj.created_at, self.obj.updated_at)
        self.obj.save()
        self.assertNotEqual(self.obj.created_at, self.obj.updated_at)

    def test_to_dict(self):
        """tests the to_dict method"""
        expected_dict = self.obj.__dict__.copy()
        expected_dict.update({'__class__': 'BaseModel'})
        expected_dict.update(
            {'created_at': expected_dict["created_at"].isoformat()})
        expected_dict.update(
            {'updated_at': expected_dict["updated_at"].isoformat()})
        self.assertDictEqual(self.obj.to_dict(), expected_dict)
        self.assertTrue(hasattr(self.obj, "__class__"))

    def test_reload_from_dict(self):
        """tests reloading an instance from dictionary"""
        self.obj.name = "My_First_Model"
        self.obj.my_number = 89
        dict_obj = self.obj.to_dict()
        obj2 = BaseModel(**dict_obj)
        self.assertEqual(self.obj.__str__(), obj2.__str__())
        self.assertIsNone(obj2.__dict__.get("__class__"))
        self.assertTrue(type(obj2.__dict__.get("created_at")) is datetime)
        self.assertTrue(type(obj2.__dict__.get("updated_at")) is datetime)
        self.assertTrue(hasattr(obj2, "my_number"))
        obj3 = BaseModel(**{})
        self.assertTrue(hasattr(obj3, "id"))
    def test_child_save(self):
        """Test subclass save method"""
        obj4 = User()
        obj4.save()
        with open("file.json") as f:            
            self.assertIn("User." + obj4.id, f.read())



if __name__ == '__main__':
    unittest.main()
