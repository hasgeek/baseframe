# -*- coding: utf-8 -*-

import unittest
from coaster.utils import LabeledEnum
from baseframe import __
from baseframe import baseframe
import baseframe.forms as forms
from .fixtures import app1 as app


class MY_LENUM(LabeledEnum):
    FIRST = (1, 'first', __("First"))
    SECOND = (2, 'second', __("Second"))
    THIRD = (3, 'third', __("Third"))


class MyForm(forms.Form):
    position = forms.EnumSelectField(__("Position"), lenum=MY_LENUM, default=MY_LENUM.THIRD)


class TestFormSQLAlchemy(unittest.TestCase):
    def setUp(self):
        baseframe.init_app(app, requires=['baseframe'])
        self.ctx = app.test_request_context()
        self.ctx.push()
        self.form = MyForm(meta={'csrf': False})

    def tearDown(self):
        self.ctx.pop()

    def test_enumfield(self):
        self.assertEqual(self.form.position.data, 'third')  # because nor yet validated
        self.form.process(position=u'second')
        self.assertTrue(self.form.validate())
        self.assertEqual(self.form.position.data, 2)

        self.form.process(position=u'forth')
        self.assertFalse(self.form.validate())
