from bravado_core.spec import Spec
from bravado_core.unmarshal import unmarshal_schema_object


def test_missing_spec_true(minimal_swagger_dict):
    swagger_spec = Spec.from_dict(
                        minimal_swagger_dict,
                        config={'pass_property_on_missing_spec': True})
    object_spec = {
        'type': 'object',
        'properties': {
            'name': {
                'type': 'string',
            },
        }
    }

    result = unmarshal_schema_object(
        swagger_spec,
        object_spec,
        {'name': 'name', 'title': 'title'})
    assert 'title' in result
    assert 'name' in result


def test_missing_spec_false(minimal_swagger_dict):
    swagger_spec = Spec.from_dict(
                        minimal_swagger_dict,
                        config={'pass_property_on_missing_spec': False})
    object_spec = {
        'type': 'object',
        'properties': {
            'name': {
                'type': 'string',
            },
        }
    }

    result = unmarshal_schema_object(
        swagger_spec,
        object_spec,
        {'name': 'name', 'title': 'title'})
    assert 'title' not in result
    assert 'name' in result
