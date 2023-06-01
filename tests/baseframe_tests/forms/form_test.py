"""Test forms."""
# pylint: disable=redefined-outer-name

from werkzeug.datastructures import MultiDict
import pytest

from baseframe import forms
from baseframe.filters import render_field_options

# Fake password hasher, only suitable for re-use within a single process
password_hash = hash


class SimpleUser:
    fullname: str
    company: str
    pw_hash: str

    def _set_password(self, value):
        self.pw_hash = password_hash(value)

    password = property(fset=_set_password)

    def __init__(self, fullname, company, password):
        self.fullname = fullname
        self.company = company
        self.password = password

    def password_is(self, candidate):
        return self.pw_hash == password_hash(candidate)


class GetSetForm(forms.Form):
    firstname = forms.StringField("First name")
    lastname = forms.StringField("Last name")
    company = forms.StringField("Company")  # Test for NOT having get_/set_company
    password = forms.PasswordField("Password")
    confirm_password = forms.PasswordField("Confirm password")

    def get_firstname(self, obj):
        return obj.fullname.split(' ', 1)[0]

    def get_lastname(self, obj):
        parts = obj.fullname.split(' ', 1)
        if len(parts) > 1:
            return parts[-1]
        return ''

    def get_password(self, obj):
        return ''

    def get_confirm_password(self, obj):
        return ''

    def set_firstname(self, obj):
        pass

    def set_lastname(self, obj):
        obj.fullname = self.firstname.data + " " + self.lastname.data

    def set_password(self, obj):
        obj.password = self.password.data

    def set_confirm_password(self, obj):
        pass


class InitOrderForm(forms.Form):
    __expects__ = ('expected_item',)

    has_context = forms.StringField("Has context")

    def get_has_context(self, obj):
        return self.expected_item


class FieldRenderForm(forms.Form):
    string_field = forms.StringField("String")


@pytest.fixture()
def user():
    return SimpleUser(  # nosec
        fullname="Test user", company="Test company", password="test"
    )


@pytest.mark.usefixtures('ctx')
def test_no_obj() -> None:
    """Test that the form can be initialized without an object."""
    form = GetSetForm(meta={'csrf': False})

    # Confirm form is bkank
    assert form.firstname.data is None
    assert form.lastname.data is None
    assert form.company.data is None
    assert form.password.data is None
    assert form.confirm_password.data is None


@pytest.mark.usefixtures('ctx')
def test_get(user) -> None:
    """Test that the form loads values from the provided object."""
    form = GetSetForm(obj=user, meta={'csrf': False})

    # Confirm form loaded from user object
    assert form.firstname.data == "Test"
    assert form.lastname.data == "user"
    assert form.company.data == "Test company"
    assert form.password.data == ''
    assert form.confirm_password.data == ''


@pytest.mark.usefixtures('ctx')
def test_get_formdata(user) -> None:
    """Test that the form preferentially loads from form data."""
    form = GetSetForm(
        formdata=MultiDict(
            {
                'firstname': "Ffirst",
                'lastname': "Flast",
                'company': "Form company",
                'password': "Test123",
                'confirm_password': "Mismatched",
            }
        ),
        obj=user,
        meta={'csrf': False},
    )

    # Confirm form loaded from formdata instead of user object
    assert form.firstname.data == "Ffirst"
    assert form.lastname.data == "Flast"
    assert form.company.data == "Form company"
    assert form.password.data == "Test123"
    assert form.confirm_password.data == "Mismatched"


@pytest.mark.usefixtures('ctx')
def test_set(user) -> None:
    """Test that the form populates an object with or without set methods."""
    form = GetSetForm(
        formdata=MultiDict(
            {
                'firstname': "Ffirst",
                'lastname': "Flast",
                'company': "Form company",
                'password': "Test123",
                'confirm_password': "Mismatched",
            }
        ),
        obj=user,
        meta={'csrf': False},
    )

    # Check user object before and after populating
    assert user.fullname == "Test user"
    assert user.company == "Test company"
    assert user.password_is("test")

    form.populate_obj(user)

    assert user.fullname == "Ffirst Flast"
    assert user.company == "Form company"
    assert not user.password_is("test")
    assert user.password_is("Test123")
    assert not hasattr(user, 'confirm_password')


@pytest.mark.usefixtures('ctx')
def test_init_order() -> None:
    """Test that get_<fieldname> methods have proper context."""
    with pytest.raises(TypeError):
        # A parameter named `expected_item` is expected
        InitOrderForm(meta={'csrf': False})

    # get_<fieldname> is only called when there is an object
    form = InitOrderForm(expected_item='probe', meta={'csrf': False})
    assert form.has_context.data is None

    # get_<fieldname> has context when it is called
    form = InitOrderForm(expected_item='probe', obj=object(), meta={'csrf': False})
    assert form.has_context.data == 'probe'


@pytest.mark.usefixtures('ctx')
def test_render_field_options() -> None:
    form = FieldRenderForm(meta={'csrf': False})
    test_attrs = {
        'attrone': 'test',
        'attrtwo': False,
        'attrthree': None,
        'attrfour': '',
    }
    render = render_field_options(form.string_field, **test_attrs)
    # This expicit rendering is based on dictionary key order stability in Python 3.7+
    assert render == (
        '<input'
        ' attrfour="" attrone="test"'
        ' id="string_field" name="string_field" type="text" value="">'
    )
