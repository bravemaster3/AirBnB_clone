#!/usr/bin/python3
"""
This module defines User Class
"""

from models.base_model import BaseModel


class User(BaseModel):
    """Definition of User class"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
