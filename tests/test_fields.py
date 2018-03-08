# -*- coding: utf-8 -*-

import unittest
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


class EnumSelectForm(forms.Form):
    position = forms.EnumSelectField(__("Position"), lenum=MY_ENUM, default=MY_ENUM.THIRD)
    position_no_default = forms.EnumSelectField(__("Position Without Default"), lenum=MY_ENUM)


class TestEnumField(unittest.TestCase):
    def setUp(self):
        self.ctx = app.test_request_context()
        self.ctx.push()
        self.form = EnumSelectForm(meta={'csrf': False})

    def tearDown(self):
        self.ctx.pop()

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
