# -*- coding: utf-8 -*-

from datetime import datetime
from decimal import Decimal
import unittest

from werkzeug.datastructures import MultiDict

from baseframe import __
from coaster.utils import LabeledEnum
import baseframe.forms as forms

from .fixtures import app1 as app


class MY_ENUM(LabeledEnum):  # NOQA: N801
    FIRST = (1, 'first', __("First"))
    SECOND = (2, 'second', __("Second"))
    THIRD = (3, 'third', __("Third"))

    __order__ = (FIRST, SECOND, THIRD)


DEFAULT_JSONDATA = {'key': u"val"}


class EnumForm(forms.Form):
    position = forms.EnumSelectField(
        __("Position"), lenum=MY_ENUM, default=MY_ENUM.THIRD
    )
    position_no_default = forms.EnumSelectField(
        __("Position Without Default"), lenum=MY_ENUM
    )


class JsonForm(forms.Form):
    jsondata = forms.JsonField("JSON Data", default=DEFAULT_JSONDATA)
    jsondata_empty_default = forms.JsonField("JSON Data", default={})
    jsondata_no_default = forms.JsonField("JSON No Default")
    jsondata_no_dict = forms.JsonField("JSON No Dict", require_dict=False)
    jsondata_no_decimal = forms.JsonField("JSON No Decimal", use_decimal=False)


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.ctx = app.test_request_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()


class TestEnumField(BaseTestCase):
    def setUp(self):
        super(TestEnumField, self).setUp()
        self.form = EnumForm(meta={'csrf': False})

    def test_default(self):
        assert self.form.position.data == 3
        assert self.form.position_no_default.data is None

    def test_process_valid(self):
        self.form.process(
            formdata=MultiDict({'position': 'second', 'position_no_default': 'third'})
        )
        assert self.form.validate() is True

        assert self.form.position.data == 2
        assert self.form.position_no_default.data == 3

    def test_process_invalid(self):
        self.form.process(formdata=MultiDict({'position': 'fourth'}))
        assert self.form.validate() is False

    def test_render(self):
        assert (
            self.form.position()
            == '<select id="position" name="position"><option value="first">First</option><option value="second">Second</option><option selected value="third">Third</option></select>'
        )
        assert (
            self.form.position_no_default()
            == '<select id="position_no_default" name="position_no_default"><option value="first">First</option><option value="second">Second</option><option value="third">Third</option></select>'
        )


class TestJsonField(BaseTestCase):
    def setUp(self):
        super(TestJsonField, self).setUp()
        self.form = JsonForm(meta={'csrf': False})

    def test_default(self):
        assert self.form.jsondata.data == DEFAULT_JSONDATA
        assert self.form.jsondata_empty_default.data == {}
        assert self.form.jsondata_no_default.data is None

    def test_valid(self):
        self.form.process(formdata=MultiDict({'jsondata': '{"key": "val"}'}))
        assert self.form.validate() is True

    def test_invalid(self):
        self.form.process(
            formdata=MultiDict({'jsondata': '{"key"; "val"}'})
        )  # invalid JSON
        assert self.form.validate() is False

    def test_empty_default(self):
        self.form.process(
            formdata=MultiDict(
                {
                    'jsondata': '',
                    'jsondata_no_default': '',
                    'jsondata_empty_default': '',
                }
            )
        )
        assert self.form.jsondata.data == DEFAULT_JSONDATA
        assert self.form.jsondata_empty_default.data == {}
        assert self.form.jsondata_no_default.data is None

    def test_nondict(self):
        self.form.process(formdata=MultiDict({'jsondata': '43'}))
        assert self.form.validate() is False
        self.form.process(formdata=MultiDict({'jsondata': 'true'}))
        assert self.form.validate() is False

        self.form.process(formdata=MultiDict({'jsondata_no_dict': '43'}))
        assert self.form.validate() is True
        self.form.process(formdata=MultiDict({'jsondata_no_dict': 'true'}))
        assert self.form.validate() is True

    def test_unicode(self):
        self.form.process(formdata=MultiDict({'jsondata': u'{"key": "val😡"}'}))
        assert self.form.validate() is True
        assert self.form.jsondata.data == {"key": u"val😡"}

    def test_unicode_dumps(self):
        self.form.jsondata.data = {"key": u"val😡"}
        assert self.form.jsondata._value() == u'{\n  "key": "val😡"\n}'

    def test_decimal(self):
        self.form.jsondata.data = {"key": Decimal('1.2')}
        assert self.form.validate() is True
        assert self.form.jsondata._value() == '{\n  "key": 1.2\n}'

        self.form.process(formdata=MultiDict({'jsondata': '{"key": 1.2}'}))
        assert self.form.validate() is True
        assert self.form.jsondata.data == {"key": Decimal('1.2')}

        self.form.jsondata_no_decimal.data = {"key": Decimal('1.2')}
        with self.assertRaises(TypeError):
            self.form.jsondata_no_decimal._value()

        self.form.process(formdata=MultiDict({'jsondata_no_decimal': '{"key": 1.2}'}))
        assert self.form.validate() is True
        assert self.form.jsondata_no_decimal.data == {"key": 1.2}

    def test_array(self):
        self.form.process(
            formdata=MultiDict({'jsondata': u'[{"key": "val"}, {"key2": "val2"}]'})
        )
        assert self.form.validate() is False

        self.form.process(
            formdata=MultiDict(
                {'jsondata_no_dict': u'[{"key": "val"}, {"key2": "val2"}]'}
            )
        )
        assert self.form.validate() is True
        assert self.form.jsondata_no_dict.data == [{"key": "val"}, {"key2": "val2"}]

    def test_comment(self):
        self.form.process(
            formdata=MultiDict(
                {
                    'jsondata': u"""
            {
                "key": "val" # test comment
            }
            """
                }
            )
        )
        assert self.form.validate() is False

    def test_non_serializable(self):
        self.form.jsondata.data = {"key": datetime.now()}
        with self.assertRaises(TypeError):
            self.form.jsondata._value()

    def test_escaped_label_text(self):
        label = forms.Label('test', '<script>alert("test");</script>')
        self.assertEqual(
            label(for_='foo'),
            """<label for="foo">&lt;script&gt;alert(&#34;test&#34;);&lt;/script&gt;</label>""",
        )
        self.assertEqual(
            label(**{'for': 'bar'}),
            """<label for="bar">&lt;script&gt;alert(&#34;test&#34;);&lt;/script&gt;</label>""",
        )
