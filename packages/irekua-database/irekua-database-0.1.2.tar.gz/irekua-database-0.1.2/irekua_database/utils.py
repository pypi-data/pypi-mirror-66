from hashlib import sha256

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import jsonschema


GENERIC_SAMPLING_EVENT = _('generic sampling event')
GENERIC_SITE = _('generic site')
GENERIC_COLLECTION = _('generic collection')

SIMPLE_JSON_SCHEMA = {}


def validate_JSON_schema(schema):
    try:
        jsonschema.validate(schema=schema, instance={})
    except jsonschema.exceptions.SchemaError as error:
        msg = _('JSON Schema is not valid. Error: %(error)s')
        params = dict(error=error)
        raise ValidationError(msg, params=params)
    except jsonschema.exceptions.ValidationError:
        pass


def validate_JSON_instance(schema=None, instance=None):
    try:
        jsonschema.validate(schema=schema, instance=instance)
    except jsonschema.exceptions.ValidationError as error:
        msg = _('Instance does not comply with JSON schema. Error: %(error)s')
        params = dict(error=error.message)
        raise ValidationError(msg, params=params)


def simple_JSON_schema():
    return SIMPLE_JSON_SCHEMA.copy()


def empty_JSON():
    return {}


def hash_file(item_file, block_size=65536):
    hasher = sha256()
    while True:
        data = item_file.read(block_size)
        if not data:
            break
        hasher.update(data)
    return hasher.hexdigest()


def translate_doc(cls):
    cls.__doc__ = cls.help_text
    return cls
