import pytest

from bravado_core.spec import Spec
from bravado_core.unmarshal import unmarshal_schema_object


@pytest.fixture
def include_read_only_properties_false():
    return {
        'include_read_only_properties': False,
        'expand_missing_properties': False
    }


@pytest.fixture
def include_read_only_properties_true():
    return {
        'include_read_only_properties': True,
        'expand_missing_properties': False
    }


@pytest.fixture
def unmarshall_simple_read_only_object_dict():
    return {
        'type': 'object',
        'properties': {
            'name': {
                'type': 'string',
                'readOnly': True
            },
            'title': {
                'type': 'string',
            },
        }
    }


def test_unmarshall_read_only_true(minimal_swagger_dict,
                                   include_read_only_properties_false,
                                   unmarshall_simple_read_only_object_dict):
    swagger_spec = Spec.from_dict(
                        minimal_swagger_dict,
                        config=include_read_only_properties_false)

    result = unmarshal_schema_object(
        swagger_spec,
        unmarshall_simple_read_only_object_dict,
        {'name': 'name', 'title': 'title'})
    assert 'name' not in result
    assert 'title' in result


def test_unmarshall_read_only_false(minimal_swagger_dict,
                                    include_read_only_properties_true,
                                    unmarshall_simple_read_only_object_dict):
    swagger_spec = Spec.from_dict(
                        minimal_swagger_dict,
                        config=include_read_only_properties_true)

    result = unmarshal_schema_object(
        swagger_spec,
        unmarshall_simple_read_only_object_dict,
        {'name': 'name', 'title': 'title'})
    assert result['name'] == 'name'
    assert 'title' in result
