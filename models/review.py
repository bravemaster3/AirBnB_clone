#!/usr/bin/python3
"""
This module defines Review Class
"""

from models.base_model import BaseModel


class Review(BaseModel):
    """Definition of Review class"""
    place_id = ""
    user_id = ""
    text = ""
