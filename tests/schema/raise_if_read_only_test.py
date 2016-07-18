import pytest

from bravado_core.schema import raise_if_read_only, SwaggerReadOnly
from bravado_core.spec import Spec


@pytest.fixture
def raise_if_read_only_true():
    return {'type': 'integer', 'readOnly': True}


@pytest.fixture
def raise_if_read_only_false():
    return {'type': 'integer', 'readOnly': False}


@pytest.fixture
def include_read_only_properties_true():
    return {'include_read_only_properties': True}


@pytest.fixture
def include_read_only_properties_false():
    return {'include_read_only_properties': False}


def test_read_only_true_do_not_include(minimal_swagger_dict,
                                       raise_if_read_only_true,
                                       include_read_only_properties_false):
    swagger_spec = Spec(minimal_swagger_dict,
                        config=include_read_only_properties_false)
    with pytest.raises(SwaggerReadOnly):
        raise_if_read_only(swagger_spec, raise_if_read_only_true)


def test_read_only_true_include(minimal_swagger_dict,
                                raise_if_read_only_true,
                                include_read_only_properties_true):
    swagger_spec = Spec(minimal_swagger_dict,
                        config=include_read_only_properties_true)
    raise_if_read_only(swagger_spec, raise_if_read_only_true)


def test_read_only_false_do_not_include(minimal_swagger_dict,
                                        raise_if_read_only_false,
                                        include_read_only_properties_false):
    swagger_spec = Spec(minimal_swagger_dict,
                        config=include_read_only_properties_false)
    raise_if_read_only(swagger_spec, raise_if_read_only_false)


def test_read_only_false_include(minimal_swagger_dict,
                                 raise_if_read_only_false,
                                 include_read_only_properties_true):
    swagger_spec = Spec(minimal_swagger_dict,
                        config=include_read_only_properties_true)
    raise_if_read_only(swagger_spec, raise_if_read_only_false)


def test_defaults_to_false(minimal_swagger_spec):
    raise_if_read_only(minimal_swagger_spec,
                       {'type': 'integer', 'readOnly': True})


def test_ref_true(minimal_swagger_dict,
                  raise_if_read_only_true,
                  include_read_only_properties_true):
    minimal_swagger_dict['definitions']['Foo'] = raise_if_read_only_true
    swagger_spec = Spec(minimal_swagger_dict,
                        config=include_read_only_properties_true)
    raise_if_read_only(swagger_spec, {'$ref': '#/definitions/Foo'})


def test_ref_false(minimal_swagger_dict,
                   raise_if_read_only_true,
                   include_read_only_properties_false):
    minimal_swagger_dict['definitions']['Foo'] = raise_if_read_only_true
    swagger_spec = Spec(minimal_swagger_dict,
                        config=include_read_only_properties_false)
    with pytest.raises(SwaggerReadOnly):
        raise_if_read_only(swagger_spec, {'$ref': '#/definitions/Foo'})


def test_ref_default_to_false(minimal_swagger_dict):
    minimal_swagger_dict['definitions']['Foo'] = {'type': 'integer'}
    swagger_spec = Spec.from_dict(minimal_swagger_dict)
    raise_if_read_only(swagger_spec, {'$ref': '#/definitions/Foo'})
