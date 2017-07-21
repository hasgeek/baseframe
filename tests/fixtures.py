import unittest
from flask import Flask
from baseframe import baseframe, forms


class BaseframeTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        baseframe.init_app(self.app, requires=['baseframe'])


class TestUser(object):
    def __init__(self, avatar=None, email=None):
        self.avatar = self.set_avatar(avatar)
        self.email = self.set_email(email)

    def set_avatar(self, avatar):
        self.avatar = avatar

    def set_email(self, email):
        self.email = email


class TestForm(forms.Form):
    test_field = forms.IntegerField("Test label", default=1)
