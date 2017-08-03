import unittest
from flask import Flask
from baseframe import baseframe
from baseframe import _, __
import baseframe.forms as forms


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


class TestDocument(object):
    def __init__(self, url=None, content=None):
        self.url = url
        self.content = content


class TestUrlForm(forms.Form):
    url = forms.URLField(__("URL"),
        validators=[forms.validators.DataRequired(), forms.validators.Length(max=255), forms.validators.ValidUrl()],
        filters=[forms.filters.strip()])

class TestAllUrlsForm(forms.Form):
    content_with_urls = forms.TextAreaField(__("Content"),
        validators=[forms.validators.DataRequired(), forms.validators.AllUrlsValid()])
