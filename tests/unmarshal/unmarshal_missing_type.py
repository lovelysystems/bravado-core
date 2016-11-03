from bravado_core.spec import Spec
from bravado_core.unmarshal import unmarshal_schema_object


def test_missing_type_true(minimal_swagger_dict):
    swagger_spec = Spec.from_dict(
                        minimal_swagger_dict,
                        config={})
    object_spec = {
        'type': 'object',
        'properties': {
            'name': {
                'description': 'Property without type definition'
            },
        }
    }

    values = ['a string', 42, True, None]

    for value in values:
        value = 'a string'
        result = unmarshal_schema_object(
            swagger_spec,
            object_spec,
            {'name': value})
        assert type(result['name']) == type(value)

