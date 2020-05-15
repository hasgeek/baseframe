# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import re
import unittest

from flask import Flask

from baseframe import __, baseframe, forms

app1 = Flask(__name__)
app1.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
app1.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app1.config['CACHE_TYPE'] = 'simple'
app2 = Flask(__name__)
app2.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///baseframe_test'
app2.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app2.config['CACHE_TYPE'] = 'simple'
baseframe.init_app(app1, requires=['baseframe'])
baseframe.init_app(app2, requires=['baseframe'])


class TestCaseBaseframe(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['CACHE_TYPE'] = 'simple'
        baseframe.init_app(self.app, requires=['baseframe'])


class UserTest(object):
    def __init__(self, avatar=None, email=None):
        self.avatar = self.set_avatar(avatar)
        self.email = self.set_email(email)

    def set_avatar(self, avatar):
        self.avatar = avatar

    def set_email(self, email):
        self.email = email


class FormTest(forms.Form):
    test_field = forms.IntegerField("Test label", default=1)


class DocumentTest(object):
    def __init__(self, url=None, content=None):
        self.url = url
        self.content = content


reject_list = [(['example.com', re.compile(r'example.in')], 'This URL is not allowed')]


class UrlFormTest(forms.Form):
    url = forms.URLField(
        __("URL"),
        validators=[
            forms.validators.DataRequired(),
            forms.validators.Length(max=255),
            forms.validators.ValidUrl(invalid_urls=reject_list),
        ],
        filters=[forms.filters.strip()],
    )


class EmojiFormTest(forms.Form):
    emoji = forms.StringField(__("Emoji"), validators=[forms.validators.IsEmoji()])


class AllUrlsFormTest(forms.Form):
    content_with_urls = forms.TextAreaField(
        __("Content"),
        validators=[forms.validators.DataRequired(), forms.validators.AllUrlsValid()],
    )


class PublicEmailDomainFormTest(forms.Form):
    webmail_domain = forms.StringField(
        __("Webmail Domain"), validators=[forms.validators.IsPublicEmailDomain()]
    )
    not_webmail_domain = forms.StringField(
        __("Not Webmail Domain"), validators=[forms.validators.IsNotPublicEmailDomain()]
    )
