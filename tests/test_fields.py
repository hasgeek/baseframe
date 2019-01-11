# -*- coding: utf-8 -*-

import unittest
from decimal import Decimal
from datetime import datetime
from werkzeug.datastructures import MultiDict
from coaster.utils import LabeledEnum
from baseframe import __
import baseframe.forms as forms
from .fixtures import app1 as app


class MY_ENUM(LabeledEnum):
    FIRST = (1, 'first', __("First"))
    SECOND = (2, 'second', __("Second"))
    THIRD = (3, 'third', __("Third"))

    __order__ = (FIRST, SECOND, THIRD)


DEFAULT_JSONDATA = {'key': u"val"}


class TestForm(forms.Form):
    position = forms.EnumSelectField(__("Position"), lenum=MY_ENUM, default=MY_ENUM.THIRD)
    position_no_default = forms.EnumSelectField(__("Position Without Default"), lenum=MY_ENUM)
    jsondata = forms.JsonField(__("JSON Data"), default=DEFAULT_JSONDATA)
    jsondata_no_default = forms.JsonField(__("JSON Data"))


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.ctx = app.test_request_context()
        self.ctx.push()
        self.form = TestForm(meta={'csrf': False})

    def tearDown(self):
        self.ctx.pop()


class TestEnumField(BaseTestCase):
    def test_default(self):
        assert self.form.position.data == 3
        assert self.form.position_no_default.data is None

    def test_process_valid(self):
        self.form.process(formdata=MultiDict({'position': 'second', 'position_no_default': 'third'}))
        assert self.form.validate() is True

        assert self.form.position.data == 2
        assert self.form.position_no_default.data == 3

    def test_process_invalid(self):
        self.form.process(formdata=MultiDict({'position': 'fourth'}))
        assert self.form.validate() is False

    def test_render(self):
        assert self.form.position() == '<select id="position" name="position"><option value="first">First</option><option value="second">Second</option><option selected value="third">Third</option></select>'
        assert self.form.position_no_default() == '<select id="position_no_default" name="position_no_default"><option value="first">First</option><option value="second">Second</option><option value="third">Third</option></select>'


class TestJSONField(BaseTestCase):
    def test_default(self):
        assert self.form.jsondata.data == DEFAULT_JSONDATA
        assert self.form.jsondata_no_default.data is None

    def test_valid(self):
        self.form.process(formdata=MultiDict({'jsondata': '{"key": "val"}'}))
        assert self.form.validate() is True

    def test_invalid(self):
        self.form.process(formdata=MultiDict({'jsondata': '{"key"; "val"}'}))  # invalid JSON
        assert self.form.validate() is False

    def test_unicode(self):
        self.form.process(formdata=MultiDict({'jsondata': u'{"key": "val😡"}'}))
        assert self.form.validate() is True
        assert self.form.jsondata.data == {"key": u"val😡"}

    def test_decimal(self):
        self.form.jsondata.data = {"key": Decimal('1.2')}
        assert self.form.validate() is True
        assert self.form.jsondata._value() == '{"key": 1.2}'

        self.form.process(formdata=MultiDict({'jsondata': '{"key": 1.2}'}))
        assert self.form.validate() is True
        assert self.form.jsondata.data == {"key": Decimal('1.2')}

    def test_array(self):
        self.form.process(formdata=MultiDict({'jsondata': u'[{"key": "val"}, {"key2": "val2"}]'}))
        assert self.form.validate() is True
        assert self.form.jsondata.data == [{"key": "val"}, {"key2": "val2"}]

    def test_comment(self):
        self.form.process(formdata=MultiDict({'jsondata': u"""
            {
                "key": "val" # test comment
            }
            """}))
        assert self.form.validate() is False

    def test_formatting(self):
        self.form.process(formdata=MultiDict({'jsondata': u"""
            [{
                "key": "val"
            }]
            """}))
        assert self.form.validate() is True
        assert self.form.jsondata.data == [{"key": u"val"}]

    def test_non_serializable(self):
        self.form.jsondata.data = {"key": datetime.now()}
        assert self.form.validate() is False
        with self.assertRaises(TypeError):
            self.form.jsondata._value()
