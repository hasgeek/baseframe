# -*- coding: utf-8 -*-

"""
Optional SQLAlchemy base class for blueprint-driven apps.
"""

from flask.ext.sqlalchemy import SQLAlchemy

__all__ = ['db']

db = SQLAlchemy()
