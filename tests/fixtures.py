import unittest
from flask import Flask
from baseframe import baseframe


class BaseframeTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        baseframe.init_app(self.app, requires=['baseframe'])

    def tearDown(self):
        pass


class TestUser:
    def __init__(self, avatar=None, email=None):
        self.avatar = self.set_avatar(avatar)
        self.email = self.set_email(email)

    def set_avatar(self, avatar):
        self.avatar = u'//www.gravatar.com/avatar/test'

    def set_email(self, email):
        self.email = email
