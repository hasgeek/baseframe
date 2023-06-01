"""Test form fields."""
# pylint: disable=redefined-outer-name,protected-access

from datetime import datetime
from decimal import Decimal

from pytz import timezone, utc
from werkzeug.datastructures import MultiDict
import pytest

from coaster.utils import LabeledEnum

from baseframe import forms

# --- Fixtures -------------------------------------------------------------------------


class MY_ENUM(LabeledEnum):  # noqa: N801
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


class DateTimeForm(forms.Form):
    naive = forms.DateTimeField("Date/time Field", naive=True, timezone='Asia/Kolkata')
    aware = forms.DateTimeField("Date/time Field", naive=False, timezone='Asia/Kolkata')


# --- Tests ----------------------------------------------------------------------------


@pytest.fixture()
def enum_form(ctx):
    """Enum form fixture."""
    return EnumForm(meta={'csrf': False})


def test_enum_default(enum_form) -> None:
    assert enum_form.position.data == 3
    assert enum_form.position_no_default.data is None


def test_enum_process_valid(enum_form) -> None:
    enum_form.process(
        formdata=MultiDict({'position': 'second', 'position_no_default': 'third'})
    )
    assert enum_form.validate() is True

    assert enum_form.position.data == 2
    assert enum_form.position_no_default.data == 3


def test_enum_process_invalid(enum_form) -> None:
    enum_form.process(formdata=MultiDict({'position': 'fourth'}))
    assert enum_form.validate() is False


def test_enum_render(enum_form) -> None:
    assert (
        enum_form.position()
        == '<select id="position" name="position"><option value="first">First</option>'
        '<option value="second">Second</option><option selected value="third">Third'
        '</option></select>'
    )
    assert (
        enum_form.position_no_default()
        == '<select id="position_no_default" name="position_no_default"><option'
        ' value="first">First</option><option value="second">Second</option><option'
        ' value="third">Third</option></select>'
    )


@pytest.fixture()
def json_form(ctx):
    """JSON form fixture."""
    return JsonForm(meta={'csrf': False})


def test_json_default(json_form) -> None:
    assert json_form.jsondata.data == DEFAULT_JSONDATA
    assert json_form.jsondata_empty_default.data == {}
    assert json_form.jsondata_no_default.data is None


def test_json_valid(json_form) -> None:
    json_form.process(formdata=MultiDict({'jsondata': '{"key": "val"}'}))
    assert json_form.validate() is True


def test_json_invalid(json_form) -> None:
    json_form.process(
        formdata=MultiDict({'jsondata': '{"key"; "val"}'})
    )  # invalid JSON
    assert json_form.validate() is False


def test_json_empty_default(json_form) -> None:
    json_form.process(
        formdata=MultiDict(
            {
                'jsondata': '',
                'jsondata_no_default': '',
                'jsondata_empty_default': '',
            }
        )
    )
    assert json_form.jsondata.data == DEFAULT_JSONDATA
    assert json_form.jsondata_empty_default.data == {}
    assert json_form.jsondata_no_default.data is None


def test_json_nondict(json_form) -> None:
    json_form.process(formdata=MultiDict({'jsondata': '43'}))
    assert json_form.validate() is False
    json_form.process(formdata=MultiDict({'jsondata': 'true'}))
    assert json_form.validate() is False

    json_form.process(formdata=MultiDict({'jsondata_no_dict': '43'}))
    assert json_form.validate() is True
    json_form.process(formdata=MultiDict({'jsondata_no_dict': 'true'}))
    assert json_form.validate() is True


def test_json_unicode(json_form) -> None:
    json_form.process(formdata=MultiDict({'jsondata': '{"key": "val😡"}'}))
    assert json_form.validate() is True
    assert json_form.jsondata.data == {"key": "val😡"}


def test_json_unicode_dumps(json_form) -> None:
    json_form.jsondata.data = {"key": "val😡"}
    assert json_form.jsondata._value() == '{\n  "key": "val😡"\n}'


def test_json_decimal(json_form) -> None:
    json_form.jsondata.data = {"key": Decimal('1.2')}
    assert json_form.validate() is True
    assert json_form.jsondata._value() == '{\n  "key": "1.2"\n}'

    json_form.process(formdata=MultiDict({'jsondata': '{"key": "1.2"}'}))
    assert json_form.validate() is True
    assert json_form.jsondata.data == {"key": "1.2"}

    json_form.process(formdata=MultiDict({'jsondata': '{"key": 1.2}'}))
    assert json_form.validate() is True
    assert json_form.jsondata.data == {"key": 1.2}


def test_json_array(json_form) -> None:
    json_form.process(
        formdata=MultiDict({'jsondata': '[{"key": "val"}, {"key2": "val2"}]'})
    )
    assert json_form.validate() is False

    json_form.process(
        formdata=MultiDict({'jsondata_no_dict': '[{"key": "val"}, {"key2": "val2"}]'})
    )
    assert json_form.validate() is True
    assert json_form.jsondata_no_dict.data == [{"key": "val"}, {"key2": "val2"}]


def test_json_comment(json_form) -> None:
    json_form.process(
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
    assert json_form.validate() is False


def test_json_non_serializable(json_form) -> None:
    json_form.jsondata.data = {"key": complex(1, 2)}
    with pytest.raises(TypeError):
        json_form.jsondata._value()


def test_escaped_label_text() -> None:
    label = forms.Label('test', '<script>alert("test");</script>')
    assert (
        label(for_='foo')
        == '<label for="foo">&lt;script&gt;alert(&#34;test&#34;);&lt;/script&gt;'
        '</label>'
    )
    assert (
        label(**{'for': 'bar'})
        == '<label for="bar">&lt;script&gt;alert(&#34;test&#34;);&lt;/script&gt;'
        '</label>'
    )


# The fields are marked as timezone Asia/Kolkata, so local timestamps will be cast to
# UTC with 5:30 hours removed
@pytest.mark.usefixtures('ctx')
@pytest.mark.parametrize(
    ('test_input', 'expected_naive', 'expected_aware'),
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
        (
            ['2021-06-08T10:00'],
            datetime(2021, 6, 8, 4, 30),
            datetime(2021, 6, 8, 4, 30, tzinfo=utc),
        ),
        (
            ['06/08/2021', '10:00'],  # MDY order
            datetime(2021, 6, 8, 4, 30),
            datetime(2021, 6, 8, 4, 30, tzinfo=utc),
        ),
    ],
)
def test_date_time_field(test_input, expected_naive, expected_aware) -> None:
    """Assert various datetime inputs are recogized and processed accurately."""
    form = DateTimeForm(meta={'csrf': False})
    form.process(
        formdata=MultiDict(
            [('naive', _v) for _v in test_input] + [('aware', _v) for _v in test_input],
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


@pytest.mark.usefixtures('ctx')
@pytest.mark.parametrize(
    'test_input',
    [
        '2020-2020-2020',
        '100000-01-01',
    ],
)
def test_date_time_field_badvalue(test_input) -> None:
    """Assert bad datetime input is recorded as a ValidationError."""
    form = DateTimeForm(meta={'csrf': False})
    form.process(formdata=MultiDict({'naive': test_input, 'aware': test_input}))
    form.validate()
    assert form.naive.errors == [form.naive.message]
    assert form.aware.errors == [form.aware.message]


@pytest.mark.usefixtures('ctx')
def test_date_time_field_timezone() -> None:
    """Assert timezone in DateTimeField is an object."""
    form = DateTimeForm(meta={'csrf': False})
    assert form.naive.timezone == timezone('Asia/Kolkata')
    assert form.aware.timezone == timezone('Asia/Kolkata')
    form.naive.timezone = None
    assert form.naive.timezone is not None  # Picked up from get_timezone
