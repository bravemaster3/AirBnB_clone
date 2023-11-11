#!/usr/bin/python3
"""
package initialization procedures
"""

from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
