"""Test SQLAlchemy fields."""
# pylint: disable=redefined-outer-name

import pytest
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from coaster.sqlalchemy import ModelBase, Query

from baseframe import forms

# --- Fixtures -------------------------------------------------------------------------


class Model(ModelBase, DeclarativeBase):
    """Model base class."""


db = SQLAlchemy(metadata=Model.metadata)
Model.init_flask_sqlalchemy(db)


class Document(Model):
    """Document model."""

    # pylint: disable=no-member
    __tablename__ = 'container'
    query_class = Query
    pkey = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(80), nullable=True)
    title = db.Column(db.Unicode(80), nullable=True)
    content = db.Column(db.Unicode(250))


class DocumentForm(forms.Form):
    name = forms.StringField("Name", validators=[forms.AvailableName()])
    title = forms.StringField("Title", validators=[forms.AvailableAttr('title')])
    content = forms.TextAreaField("Content")


@pytest.fixture()
def database(app):
    """Database structure."""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()


@pytest.fixture()
def db_session(database):
    """Database session fixture."""
    savepoint = database.session.begin_nested()
    yield database.session
    savepoint.rollback()
    database.session.rollback()


@pytest.fixture()
def form(ctx):
    return DocumentForm(model=Document, meta={'csrf': False})


def test_available_attr(form, db_session) -> None:
    """Test AvailableAttr SQLAlchemy validator."""
    d1 = Document()
    form.process(name='d1', title='t1')
    assert form.validate()
    form.populate_obj(d1)
    db_session.add(d1)

    d2 = Document()
    form.process(name='d2', title='t1')
    # title 't1' is repeated
    assert not form.validate()
    form.process(name='d2', title='t2')
    assert form.validate()
    form.populate_obj(d2)
    db_session.add(d2)

    d3 = Document()
    form.process(name='d2', title='t3')
    # name 'd2' repeated
    assert not form.validate()
    form.process(name='d3', title='t3')
    form.populate_obj(d3)
    db_session.add(d3)
