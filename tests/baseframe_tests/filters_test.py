"""Test form filters."""
# pylint: disable=redefined-outer-name

import typing as t
from datetime import date, datetime, time, timedelta
from types import SimpleNamespace

import pytest
from pytz import UTC, timezone

from coaster.utils import md5sum

from baseframe import filters


@pytest.fixture(params=[True, False])
def times(request):
    """Sample times fixture."""
    now = datetime.now(UTC) if request.param else datetime.utcnow()
    return SimpleNamespace(
        now=now,
        date=date(2020, 1, 31),
        datetime=datetime(2020, 1, 31, 0, 0, tzinfo=timezone("UTC")),
        time=time(23, 59, 59),
        datetimeEST=datetime(2020, 1, 31, 0, 0, tzinfo=timezone("America/New_York")),
    )


def test_dt_filters_age(times) -> None:
    age = filters.age(times.now)
    assert age == 'now'

    nine_seconds = times.now - timedelta(seconds=9)
    age = filters.age(nine_seconds)
    assert age == 'seconds ago'

    thirty_minutes = times.now - timedelta(minutes=30)
    age = filters.age(thirty_minutes)
    assert age == '30 minutes ago'

    one_half_hour = times.now - timedelta(hours=1.5)
    age = filters.age(one_half_hour)
    assert age == 'an hour ago'

    ten_months = times.now - timedelta(days=10 * 30)
    age = filters.age(ten_months)
    assert age == '10 months ago'

    three_years = times.now - timedelta(days=3 * 12 * 30)
    age = filters.age(three_years)
    assert age == '2 years ago'


def test_dt_filters_shortdate_date_with_threshold(app, times) -> None:
    app.config['SHORTDATE_THRESHOLD_DAYS'] = 10
    testdate = times.now.date() - timedelta(days=5)
    with app.test_request_context('/'):
        assert filters.shortdate(testdate) == testdate.strftime('%e %b')


def test_dt_filters_shortdate_date_without_threshold(app, times) -> None:
    app.config['SHORTDATE_THRESHOLD_DAYS'] = 0
    testdate = times.now.date() - timedelta(days=5)
    with app.test_request_context('/'):
        assert filters.shortdate(testdate).replace("’", "'") == testdate.strftime(
            "%e %b '%y"
        )


def test_dt_filters_shortdate_datetime_with_threshold(app, times) -> None:
    app.config['SHORTDATE_THRESHOLD_DAYS'] = 10
    testdate = times.now - timedelta(days=5)
    with app.test_request_context('/'):
        assert filters.shortdate(testdate) == testdate.strftime('%e %b')


def test_dt_filters_shortdate_datetime_without_threshold(app, times) -> None:
    testdate = times.now - timedelta(days=5)
    with app.test_request_context('/'):
        assert filters.shortdate(testdate).replace("’", "'") == testdate.strftime(
            "%e %b '%y"
        )


def test_dt_filters_shortdate_datetime_with_tz(app, times) -> None:
    testdate = times.now
    with app.test_request_context('/'):
        assert filters.shortdate(testdate).replace("’", "'") == testdate.strftime(
            "%e %b '%y"
        )


def test_dt_filters_longdate_date(app, times) -> None:
    testdate = times.now.date()
    with app.test_request_context('/'):
        assert filters.longdate(testdate) == testdate.strftime('%e %B %Y')


def test_dt_filters_longdate_datetime(app, times) -> None:
    testdate = times.now
    with app.test_request_context('/'):
        assert filters.longdate(testdate) == testdate.strftime('%e %B %Y')


def test_dt_filters_longdate_datetime_with_tz(app, times) -> None:
    testdate = times.now
    with app.test_request_context('/'):
        assert filters.longdate(testdate) == testdate.strftime('%e %B %Y')


def test_dt_filters_date_filter(app, times) -> None:
    with app.test_request_context('/'):
        assert (
            filters.date_filter(times.date, 'yyyy-MM-dd', usertz=False) == '2020-01-31'
        )


def test_dt_filters_date_localized_short_hi(app, times) -> None:
    with app.test_request_context('/', headers={'Accept-Language': 'hi'}):
        assert filters.date_filter(times.date, format='short') == '31/1/20'


def test_dt_filters_date_localized_medium_hi(app, times) -> None:
    with app.test_request_context('/', headers={'Accept-Language': 'hi'}):
        assert filters.date_filter(times.date, format='medium') == '31 जन॰ 2020'


def test_dt_filters_date_localized_long_hi(app, times) -> None:
    with app.test_request_context('/', headers={'Accept-Language': 'hi'}):
        assert filters.date_filter(times.date, format='long') == '31 जनवरी 2020'


def test_dt_filters_time_localized_hi_medium(app, times) -> None:
    with app.test_request_context('/', headers={'Accept-Language': 'hi'}):
        assert (
            filters.datetime_filter(times.datetime, format='medium')
            == '31 जन॰ 2020, 12:00:00 am'
        )


def test_dt_filters_month_localized_hi(app, times) -> None:
    with app.test_request_context('/', headers={'Accept-Language': 'hi'}):
        assert filters.date_filter(times.date, "MMMM") == 'जनवरी'


def test_dt_filters_month_localized_en(app, times) -> None:
    with app.test_request_context('/'):
        assert filters.date_filter(times.date, "MMMM") == 'January'


def test_dt_filters_time_localized_short(app, times) -> None:
    with app.test_request_context('/', headers={'Accept-Language': 'hi'}):
        assert filters.time_filter(times.datetime, format='short') == '12:00 am'


def test_dt_filters_time_localized_medium(app, times) -> None:
    with app.test_request_context('/', headers={'Accept-Language': 'hi'}):
        assert filters.time_filter(times.datetime, format='medium') == '12:00:00 am'


def test_dt_filters_time_localized_long(app, times) -> None:
    with app.test_request_context('/', headers={'Accept-Language': 'hi'}):
        assert filters.time_filter(times.datetime, format='long') == '12:00:00 am UTC'


def test_dt_filters_time_localized_hi_full(app, times) -> None:
    with app.test_request_context('/', headers={'Accept-Language': 'hi'}):
        assert (
            filters.time_filter(times.time, format='full')
            == '11:59:59 pm समन्वित वैश्विक समय'
        )


def test_dt_filters_time_localized_en_full(app, times) -> None:
    with app.test_request_context('/', headers={'Accept-Language': 'en'}):
        assert filters.time_filter(times.time, format='full') in (
            '11:59:59 PM Coordinated Universal Time',
            '11:59:59\u202fPM Coordinated Universal Time',
        )


def test_dt_filters_datetime_with_usertz(app, times) -> None:
    with app.test_request_context('/'):
        assert filters.datetime_filter(
            times.datetimeEST, format='full', usertz=False
        ) in (
            'Friday, January 31, 2020 at 12:00:00 AM Eastern Standard Time',
            'Friday, January 31, 2020, 12:00:00\u202fAM Eastern Standard Time',
        )


def test_dt_filters_datetime_without_usertz(app, times) -> None:
    with app.test_request_context('/'):
        assert filters.datetime_filter(
            times.datetimeEST, format='full', usertz=True
        ) in (
            'Friday, January 31, 2020 at 4:56:00 AM Coordinated Universal Time',
            'Friday, January 31, 2020, 4:56:00\u202fAM Coordinated Universal Time',
        )


def test_dt_filters_date_dmy(app, times) -> None:
    with app.test_request_context('/'):
        assert (
            filters.date_filter(times.datetime, format='short', locale='en_GB')
            == '31/01/2020'
        )


def test_dt_filters_date_mdy(app, times) -> None:
    with app.test_request_context('/'):
        assert (
            filters.date_filter(times.datetime, format='short', locale='en_US')
            == '1/31/20'
        )


def test_dt_filters_timestamp(app, times) -> None:
    with app.test_request_context('/'):
        assert filters.timestamp_filter(times.datetime) == 1580428800.0


def test_dt_filters_timestamp_filter(app, times) -> None:
    with app.test_request_context('/'):
        assert filters.timedelta_filter(times.now) == "1 second ago"
        assert filters.timedelta_filter(1) == "1 second"
        assert filters.timedelta_filter(1, format='short') == "1 sec"
        assert filters.timedelta_filter(timedelta(seconds=1)) == "1 second"
        assert filters.timedelta_filter(timedelta(days=1, hours=2)) == "1 day"
        assert filters.timedelta_filter(timedelta(days=1), format='narrow') == "1d"
        assert (
            filters.timedelta_filter(timedelta(seconds=1), add_direction=True)
            == "in 1 second"
        )
        assert (
            filters.timedelta_filter(timedelta(days=1), add_direction=True)
            == "in 1 day"
        )
        # Narrow format doesn't work for add_direction
        assert (
            filters.timedelta_filter(
                timedelta(days=1), format='narrow', add_direction=True
            )
            == "in 1 day"
        )
        assert (
            filters.timedelta_filter(-timedelta(seconds=1), add_direction=True)
            == "1 second ago"
        )
        assert (
            filters.timedelta_filter(-timedelta(days=1), add_direction=True)
            == "1 day ago"
        )
        # Narrow format doesn't work for add_direction
        assert (
            filters.timedelta_filter(
                -timedelta(days=1), format='narrow', add_direction=True
            )
            == "1 day ago"
        )


def test_dt_filters_timestamp_filter_hi(app, times) -> None:
    with app.test_request_context('/', headers={'Accept-Language': 'hi'}):
        assert filters.timedelta_filter(times.now) == "1 सेकंड पहले"
        assert filters.timedelta_filter(1) == "1 सेकंड"
        assert filters.timedelta_filter(1, format='short') == "1 से॰"
        assert filters.timedelta_filter(timedelta(seconds=1)) == "1 सेकंड"
        assert filters.timedelta_filter(timedelta(days=1, hours=2)) == "1 दिन"
        assert filters.timedelta_filter(timedelta(days=1), format='narrow') in (
            "1दिन",
            '1 द\u093f',
        )
        assert (
            filters.timedelta_filter(timedelta(seconds=1), add_direction=True)
            == "1 सेकंड में"
        )
        assert (
            filters.timedelta_filter(timedelta(days=1), add_direction=True)
            == "1 दिन में"
        )
        # Narrow format doesn't work for add_direction
        assert (
            filters.timedelta_filter(
                timedelta(days=1), format='narrow', add_direction=True
            )
            == "1 दिन में"
        )
        assert (
            filters.timedelta_filter(-timedelta(seconds=1), add_direction=True)
            == "1 सेकंड पहले"
        )
        assert (
            filters.timedelta_filter(-timedelta(days=1), add_direction=True)
            == "1 दिन पहले"
        )
        # Narrow format doesn't work for add_direction
        assert (
            filters.timedelta_filter(
                -timedelta(days=1), format='narrow', add_direction=True
            )
            == "1 दिन पहले"
        )


def test_initials() -> None:
    initial = filters.initials('A Named Example')
    assert initial == 'AE'

    initial = filters.initials('A Slightly Longer Named Example')
    assert initial == 'AE'

    initial = filters.initials(' Abnormally  Spaced Example ')
    assert initial == 'AE'

    initial = filters.initials('Example')
    assert initial == 'E'

    initial = filters.initials('एक एक्साम्पल')
    assert initial == 'एए'

    initial = filters.initials(' ')
    assert initial == ''

    initial = filters.initials('')
    assert initial == ''

    initial = filters.initials(None)
    assert initial == ''


def test_usessl(app) -> None:
    with app.test_request_context('/'):
        app.config['USE_SSL'] = False
        ssled = filters.usessl('http://hasgeek.com')
        assert ssled == 'http://hasgeek.com'

        app.config['USE_SSL'] = True
        ssled = filters.usessl('http://hasgeek.com')
        assert ssled == 'https://hasgeek.com'

        ssled = filters.usessl('hasgeek.com')
        assert ssled == 'hasgeek.com'

        ssled = filters.usessl('/static/test')
        assert ssled == 'https://localhost/static/test'


def test_nossl(app) -> None:
    with app.test_request_context('/'):
        nossled = filters.nossl('https://hasgeek.com')
        assert nossled == 'http://hasgeek.com'

        nossled = filters.nossl('hasgeek.com')
        assert nossled == 'hasgeek.com'

        nossled = filters.nossl('//hasgeek.com')
        assert nossled == 'http://hasgeek.com'


class UserTest:
    """Fixture user with an "avatar" URL column and an email address for Gravatar."""

    avatar: t.Optional[str]
    email: str

    def __init__(self, avatar=None, email=None) -> None:
        self.set_avatar(avatar)
        self.set_email(email)

    def set_avatar(self, avatar: t.Optional[str]) -> None:
        self.avatar = avatar

    def set_email(self, email: str) -> None:
        self.email = email


def test_avatar_url() -> None:
    user = UserTest()
    avatar_size = ('100', '100')
    avatar_url = '//images.hasgeek.com/embed/test'

    # user object doesn't have an email or an avatar by default
    default_avatar_url = filters.avatar_url(user)
    assert (
        default_avatar_url
        == '//www.gravatar.com/avatar/00000000000000000000000000000000?d=mm'
    )

    # testing what if the user has an avatar already
    user.set_avatar(avatar_url)
    sized_avatar_url = filters.avatar_url(user, avatar_size)
    assert sized_avatar_url == avatar_url + '?size=' + 'x'.join(avatar_size)

    # what if the user doesn't have an avatar but has an email
    user.set_avatar(None)
    user.set_email('foobar@foo.com')
    ehash = md5sum(user.email)
    sized_avatar_url = filters.avatar_url(user, avatar_size)
    assert (
        sized_avatar_url
        == '//www.gravatar.com/avatar/' + ehash + '?d=mm&s=' + 'x'.join(avatar_size)
    )


def test_firstline() -> None:
    html = "<div>this is the first line</div><div>and second line</div>"
    firstline = filters.firstline(html)
    assert firstline == "this is the first line"


def test_preview() -> None:
    # Works with plain text
    assert filters.preview("This is plain text") == "This is plain text"
    # Works with HTML
    assert (
        filters.preview("<p>Hello all,</p><p>Here is the Zoom link.")
        == "Hello all, Here is the Zoom link."
    )
    # Removes whitespace from this indented block
    assert (
        filters.preview(
            """
            <p>Hello all,</p>
            <p>Here is the Zoom link.
            """
        )
        == "Hello all, Here is the Zoom link."
    )
    # Truncates at a paragraph boundary if it falls between min and max
    assert (
        filters.preview("<p>Hello all,</p><p>Here is the Zoom link.", min=5)
        == "Hello all,"
    )
    # Truncates text when the paragraph is not between min and max boundaries
    assert (
        filters.preview("<p>Hello all,</p><p>Here is the Zoom link.", min=15, max=20)
        == "Hello all, Here is …"
    )
    # Strips HTML tags and attributes when returning text
    assert (
        filters.preview(
            """
            <p>
                <a href="https://example.org">Example.org</a> is a reserved TLD
                for tests.
            </p>
            <p>
                Anyone may use it for any example use case.
            </p>
            """
        )
        == (
            "Example.org is a reserved TLD for tests."
            " Anyone may use it for any example use case."
        )
    )
    # Counts by Unicode graphemes, not code points, to avoid mangling letters
    assert filters.preview('हिंदी टायपिंग', min=1, max=3) == 'हिंदी…'


def test_cdata() -> None:
    text = "foo bar"
    result = filters.cdata(text)
    assert result == "<![CDATA[foo bar]]>"

    text = "<![CDATA[foo bar]]>"
    result = filters.cdata(text)
    assert result == "<![CDATA[<![CDATA[foo bar]]]]><![CDATA[>]]>"


def test_cleanurl() -> None:
    assert (
        filters.cleanurl_filter("https://www.example.com/some/path/?query=value")
        == "example.com/some/path"
    )
    assert (
        filters.cleanurl_filter("//example.com/some/path/?query=value")
        == "example.com/some/path"
    )
    assert filters.cleanurl_filter("http://www.example.com/") == "example.com"
    assert filters.cleanurl_filter("https://example.com/") == "example.com"
    assert filters.cleanurl_filter("https://windows.com/") == "windows.com"
    assert filters.cleanurl_filter("//www.example.com/") == "example.com"
    assert filters.cleanurl_filter("//test/") == "test"
    # cannot process if scheme is missing and no // to begin with
    assert (
        filters.cleanurl_filter("www.example.com/some/path/")
        == "www.example.com/some/path"
    )
    assert filters.cleanurl_filter("example.com/some/path") == "example.com/some/path"
    assert filters.cleanurl_filter("foobar") == "foobar"
