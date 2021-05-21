from datetime import datetime
from decimal import Decimal
import unittest

from werkzeug.datastructures import MultiDict

from pytz import timezone, utc
import pytest

from coaster.utils import LabeledEnum
import baseframe.forms as forms

from .fixtures import app1 as app


class MY_ENUM(LabeledEnum):  # NOQA: N801
    FIRST = (1, 'first', "First")
    SECOND = (2, 'second', "Second")
    THIRD = (3, 'third', "Third")

    __order__ = (FIRST, SECOND, THIRD)


DEFAULT_JSONDATA = {'key': "val"}


class EnumForm(forms.Form):
    position = forms.EnumSelectField("Position", lenum=MY_ENUM, default=MY_ENUM.THIRD)
    position_no_default = forms.EnumSelectField(
        "Position Without Default", lenum=MY_ENUM
    )


class JsonForm(forms.Form):
    jsondata = forms.JsonField("JSON Data", default=DEFAULT_JSONDATA)
    jsondata_empty_default = forms.JsonField("JSON Data", default={})
    jsondata_no_default = forms.JsonField("JSON No Default")
    jsondata_no_dict = forms.JsonField("JSON No Dict", require_dict=False)
    jsondata_no_decimal = forms.JsonField("JSON No Decimal", use_decimal=False)


class DateTimeForm(forms.Form):
    naive = forms.DateTimeField("Date/time Field", naive=True, timezone='Asia/Kolkata')
    aware = forms.DateTimeField("Date/time Field", naive=False, timezone='Asia/Kolkata')


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.ctx = app.test_request_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()


class TestEnumField(BaseTestCase):
    def setUp(self):
        super().setUp()
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
        super().setUp()
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
        self.form.process(formdata=MultiDict({'jsondata': '{"key": "val😡"}'}))
        assert self.form.validate() is True
        assert self.form.jsondata.data == {"key": "val😡"}

    def test_unicode_dumps(self):
        self.form.jsondata.data = {"key": "val😡"}
        assert self.form.jsondata._value() == '{\n  "key": "val😡"\n}'

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
            formdata=MultiDict({'jsondata': '[{"key": "val"}, {"key2": "val2"}]'})
        )
        assert self.form.validate() is False

        self.form.process(
            formdata=MultiDict(
                {'jsondata_no_dict': '[{"key": "val"}, {"key2": "val2"}]'}
            )
        )
        assert self.form.validate() is True
        assert self.form.jsondata_no_dict.data == [{"key": "val"}, {"key2": "val2"}]

    def test_comment(self):
        self.form.process(
            formdata=MultiDict(
                {
                    'jsondata': """
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


# The fields are marked as timezone Asia/Kolkata, so local timestamps will be cast to
# UTC with 5:30 hours removed
@pytest.mark.parametrize(
    ['test_input', 'expected_naive', 'expected_aware'],
    [
        # Blank input
        ([], None, None),
        ([''], None, None),
        (['', ''], None, None),
        (
            ['2010-12-15'],
            datetime(2010, 12, 14, 18, 30),
            datetime(2010, 12, 14, 18, 30, tzinfo=utc),
        ),
        (
            ['2010-12-15T10:00'],
            datetime(2010, 12, 15, 4, 30),
            datetime(2010, 12, 15, 4, 30, tzinfo=utc),
        ),
        (
            ['2010-12-15', ''],
            datetime(2010, 12, 14, 18, 30),
            datetime(2010, 12, 14, 18, 30, tzinfo=utc),
        ),
        (
            ['2010-12-15 10:00'],
            datetime(2010, 12, 15, 4, 30),
            datetime(2010, 12, 15, 4, 30, tzinfo=utc),
        ),
        (
            ['2010-12-15', '10:00'],
            datetime(2010, 12, 15, 4, 30),
            datetime(2010, 12, 15, 4, 30, tzinfo=utc),
        ),
        (
            ['2010-12-15 ', ' 10:00 '],
            datetime(2010, 12, 15, 4, 30),
            datetime(2010, 12, 15, 4, 30, tzinfo=utc),
        ),
        (
            ['15/12/2010', '10:00'],
            datetime(2010, 12, 15, 4, 30),
            datetime(2010, 12, 15, 4, 30, tzinfo=utc),
        ),
        (
            ['12/15/2010', '10:00'],
            datetime(2010, 12, 15, 4, 30),
            datetime(2010, 12, 15, 4, 30, tzinfo=utc),
        ),
        (
            ['Dec 15 2010', '10:00'],
            datetime(2010, 12, 15, 4, 30),
            datetime(2010, 12, 15, 4, 30, tzinfo=utc),
        ),
        (
            ['Dec 15 2010', '10:00 UTC'],
            datetime(2010, 12, 15, 10, 0),
            datetime(2010, 12, 15, 10, 0, tzinfo=utc),
        ),
        (
            ['15 Dec 2010', '10:00 UTC'],
            datetime(2010, 12, 15, 10, 0),
            datetime(2010, 12, 15, 10, 0, tzinfo=utc),
        ),
    ],
)
def test_date_time_field(test_input, expected_naive, expected_aware):
    with app.app_context():
        form = DateTimeForm(meta={'csrf': False})
        form.process(
            formdata=MultiDict(
                [('naive', _v) for _v in test_input]
                + [('aware', _v) for _v in test_input],
            )
        )
        assert form.naive.data == expected_naive
        assert form.aware.data == expected_aware
        if expected_naive is not None:
            assert form.naive._value() == utc.localize(expected_naive).astimezone(
                form.naive.timezone
            ).strftime(form.naive.display_format)
        else:
            assert form.naive._value() == ''
        if expected_aware is not None:
            assert form.aware._value() == expected_aware.astimezone(
                form.aware.timezone
            ).strftime(form.aware.display_format)
        else:
            assert form.aware._value() == ''


@pytest.mark.parametrize(
    'test_input',
    [
        '2020-2020-2020',
        '100000-01-01',
    ],
)
def test_date_time_field_badvalue(test_input):
    with app.app_context():
        form = DateTimeForm(meta={'csrf': False})
        form.process(formdata=MultiDict({'naive': test_input, 'aware': test_input}))
        form.validate()
        assert form.naive.errors == [form.naive.message]
        assert form.aware.errors == [form.aware.message]


def test_date_time_field_timezone():
    with app.app_context():
        form = DateTimeForm(meta={'csrf': False})
        assert form.naive.timezone == timezone('Asia/Kolkata')
        assert form.aware.timezone == timezone('Asia/Kolkata')
        form.naive.timezone = None
        assert form.naive.timezone is not None  # Picked up from get_timezone
