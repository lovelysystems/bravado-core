from collections import Mapping

from bravado_core.exception import SwaggerMappingError


class SwaggerReadOnly(Exception):
    """Raised if a property is read only and include_read_only_properties is
    set to False in the swagger spec configuration

    This is an internal exception and is catched in the unmarshal_object
    implementation.
    """


# 'object' and 'array' are omitted since this should really be read as
# "Swagger types that map to python primitives"
SWAGGER_PRIMITIVES = (
    'integer',
    'number',
    'string',
    'boolean',
    'null',
)


def has_default(swagger_spec, schema_object_spec):
    return 'default' in swagger_spec.deref(schema_object_spec)


def get_default(swagger_spec, schema_object_spec):
    return swagger_spec.deref(schema_object_spec).get('default')


def is_required(swagger_spec, schema_object_spec):
    return swagger_spec.deref(schema_object_spec).get('required', False)


def is_read_only(swagger_spec, schema_object_spec):
    return swagger_spec.deref(schema_object_spec).get('readOnly', False)


def raise_if_read_only(swagger_spec, schema_object_spec):
    if not swagger_spec.config.get('include_read_only_properties', True) \
       and is_read_only(swagger_spec, schema_object_spec):
        raise SwaggerReadOnly()


def has_format(swagger_spec, schema_object_spec):
    return 'format' in swagger_spec.deref(schema_object_spec)


def get_format(swagger_spec, schema_object_spec):
    return swagger_spec.deref(schema_object_spec).get('format')


def is_param_spec(swagger_spec, schema_object_spec):
    return 'in' in swagger_spec.deref(schema_object_spec)


def is_prop_nullable(swagger_spec, schema_object_spec):
    return swagger_spec.deref(schema_object_spec).get('x-nullable', False)


def is_ref(spec):
    return is_dict_like(spec) and '$ref' in spec


def is_dict_like(spec):
    """
    :param spec: swagger object specification in dict form
    :rtype: boolean
    """
    return isinstance(spec, Mapping)


def is_list_like(spec):
    """No longer needed since json-ref has been excised.

    :param spec: swagger object specification in dict form
    :rtype: boolean
    """
    # TODO: check magic method instead
    return type(spec) == list


def get_spec_for_prop(swagger_spec, object_spec, object_value, prop_name):
    """Given a jsonschema object spec and value, retrieve the spec for the
     given property taking 'additionalProperties' into consideration.

    :param object_spec: spec for a jsonschema 'object' in dict form
    :param object_value: jsonschema object containing the given property. Only
        used in error message.
    :param prop_name: name of the property to retrieve the spec for

    :return: spec for the given property or None if no spec found
    :rtype: dict
    """
    deref = swagger_spec.deref

    prop_spec = deref_allOf(swagger_spec, object_spec).get(prop_name)

    if prop_spec is not None:
        return deref(prop_spec)

    additional_props = deref(object_spec).get('additionalProperties', True)

    if isinstance(additional_props, bool):
        # no spec for additional properties to conform to - this is basically
        # a way to send pretty much anything across the wire as is.
        return None

    additional_props = deref(additional_props)
    if is_dict_like(additional_props):
        # spec that all additional props MUST conform to
        return additional_props

    raise SwaggerMappingError(
        "Don't know what to do with `additionalProperties` in spec {0} "
        "when inspecting value {1}".format(object_spec, object_value))


def deref_allOf(swagger_spec, spec):
    """Dereferencing 'allOf' to get all properties
    """
    result = {}
    spec_deref = swagger_spec.deref(spec)
    if 'properties' in spec_deref:
        result.update(spec_deref['properties'])
    elif 'allOf' in spec_deref:
        # resolve allOf into
        for c in spec_deref['allOf']:
            result.update(deref_allOf(swagger_spec, c))
    return result
