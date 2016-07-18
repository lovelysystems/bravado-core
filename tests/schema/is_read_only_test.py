import pytest

from bravado_core.schema import is_read_only
from bravado_core.spec import Spec


@pytest.fixture
def is_read_only_true():
    return {'type': 'integer', 'readOnly': True}


@pytest.fixture
def is_read_only_false():
    return {'type': 'integer', 'readOnly': False}


def test_true(minimal_swagger_spec, is_read_only_true):
    assert is_read_only(minimal_swagger_spec, is_read_only_true)


def test_false(minimal_swagger_spec, is_read_only_false):
    assert not is_read_only(minimal_swagger_spec, is_read_only_false)


def test_defaults_to_false(minimal_swagger_spec):
    assert not is_read_only(minimal_swagger_spec, {'type': 'integer'})


def test_ref_true(minimal_swagger_dict, is_read_only_true):
    minimal_swagger_dict['definitions']['Foo'] = is_read_only_true
    swagger_spec = Spec(minimal_swagger_dict)
    assert is_read_only(swagger_spec, {'$ref': '#/definitions/Foo'})


def test_ref_false(minimal_swagger_dict, is_read_only_false):
    minimal_swagger_dict['definitions']['Foo'] = is_read_only_false
    swagger_spec = Spec(minimal_swagger_dict)
    assert not is_read_only(swagger_spec, {'$ref': '#/definitions/Foo'})


def test_ref_default_to_false(minimal_swagger_dict):
    minimal_swagger_dict['definitions']['Foo'] = {'type': 'integer'}
    swagger_spec = Spec.from_dict(minimal_swagger_dict)
    assert not is_read_only(swagger_spec, {'$ref': '#/definitions/Foo'})
