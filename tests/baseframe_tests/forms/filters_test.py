"""Tests for form filters."""

from baseframe import forms


def test_lower():
    lower_func = forms.lower()
    assert lower_func('TEST') == 'test'
    assert lower_func('Test') == 'test'
    assert lower_func('') == ''


def test_upper():
    upper_func = forms.upper()
    assert upper_func('Test') == 'TEST'
    assert upper_func('test') == 'TEST'
    assert upper_func('') == ''


def test_strip():
    strip_func = forms.strip()
    assert strip_func(' Test ') == 'Test'
    assert strip_func('a       test   ') == 'a       test'
    assert strip_func('      ') == ''


def test_lstrip():
    lstrip_func = forms.lstrip()
    assert lstrip_func(' Test ') == 'Test '
    assert lstrip_func('a       test   ') == 'a       test   '
    assert lstrip_func('      ') == ''


def test_rstrip():
    rstrip_func = forms.rstrip()
    assert rstrip_func(' Test ') == ' Test'
    assert rstrip_func('a       test   ') == 'a       test'
    assert rstrip_func('      ') == ''


def test_strip_each():
    strip_each_func = forms.strip_each()
    assert strip_each_func(None) is None
    assert strip_each_func([]) == []
    assert strip_each_func(
        [' Left strip', 'Right strip ', ' Full strip ', '', 'No strip', '']
    ) == ['Left strip', 'Right strip', 'Full strip', 'No strip']


def test_none_if_empty():
    none_if_empty_func = forms.none_if_empty()
    assert none_if_empty_func('Test') == 'Test'
    assert none_if_empty_func('') is None
    assert none_if_empty_func([]) is None
    assert none_if_empty_func(False) is None
    assert none_if_empty_func(0) is None
