from bravado_core.spec import Spec
from bravado_core.unmarshal import unmarshal_schema_object


def test_missing_properties_true(minimal_swagger_dict):
    swagger_spec = Spec.from_dict(
                        minimal_swagger_dict,
                        config={'expand_missing_properties': True})
    object_spec = {
        'type': 'object',
        'properties': {
            'name': {
                'type': 'string',
            },
            'title': {
                'type': 'string',
            },
        }
    }

    result = unmarshal_schema_object(
        swagger_spec,
        object_spec,
        {'title': 'title'})
    assert result['name'] is None
    assert 'title' in result


def test_missing_properties_false(minimal_swagger_dict):
    swagger_spec = Spec.from_dict(
                        minimal_swagger_dict,
                        config={'expand_missing_properties': False})
    object_spec = {
        'type': 'object',
        'properties': {
            'name': {
                'type': 'string',
            },
            'title': {
                'type': 'string',
            },
        }
    }

    result = unmarshal_schema_object(
        swagger_spec,
        object_spec,
        {'title': 'title'})
    assert 'name' not in result
    assert 'title' in result
