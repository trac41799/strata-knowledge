#!/usr/bin/env python3
"""Minimal JSON Schema validator covering the subset used by Strata schemas.

Supported keywords: type (incl. list of types), properties, required,
additionalProperties (bool or schema), items (schema or list), enum, const,
pattern, format (date, date-time), minLength, maxLength, minItems, maxItems,
minimum, maximum, oneOf, anyOf. Other keywords are ignored.
"""

import re


def _type_matches(actual, expected):
    if actual == expected:
        return True
    return expected == 'number' and actual == 'integer'


def _type_of(v):
    if isinstance(v, bool):
        return 'boolean'
    if isinstance(v, int):
        return 'integer'
    if isinstance(v, float):
        return 'number'
    if isinstance(v, str):
        return 'string'
    if isinstance(v, list):
        return 'array'
    if isinstance(v, dict):
        return 'object'
    if v is None:
        return 'null'
    return 'unknown'


def _valid_date(s):
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', s):
        return False
    year, month, day = (int(x) for x in s.split('-'))
    if month < 1 or month > 12:
        return False
    if day < 1 or day > 31:
        return False
    if month in (4, 6, 9, 11) and day > 30:
        return False
    if month == 2:
        leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
        if day > (29 if leap else 28):
            return False
    return True


def _valid_datetime(s):
    return re.fullmatch(
        r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})?', s
    ) is not None


def validate(instance, schema, path='$', errors=None):
    if errors is None:
        errors = []
    if not isinstance(schema, dict):
        raise TypeError('schema must be an object')
    if 'oneOf' in schema:
        matches = 0
        for sub in schema['oneOf']:
            sub_errors = validate(instance, sub, path, [])
            if not sub_errors:
                matches += 1
        if matches != 1:
            errors.append('%s: matches %d of oneOf branches (expected exactly 1)' % (path, matches))
    if 'anyOf' in schema:
        matches = 0
        for sub in schema['anyOf']:
            sub_errors = validate(instance, sub, path, [])
            if not sub_errors:
                matches += 1
        if matches < 1:
            errors.append('%s: matches no anyOf branch' % path)
    t = schema.get('type')
    if t:
        actual = _type_of(instance)
        if isinstance(t, list):
            if not any(_type_matches(actual, expected) for expected in t):
                errors.append('%s: expected type in %s, got %s' % (path, t, actual))
        elif not _type_matches(actual, t):
            errors.append('%s: expected type %s, got %s' % (path, t, actual))
    if 'const' in schema and instance != schema['const']:
        errors.append('%s: expected const %r' % (path, schema['const']))
    if 'enum' in schema and instance not in schema['enum']:
        errors.append('%s: %r not in enum %s' % (path, instance, schema['enum']))
    if isinstance(instance, str):
        if 'pattern' in schema and not re.search(schema['pattern'], instance):
            errors.append('%s: %r does not match pattern %r' % (path, instance, schema['pattern']))
        if 'minLength' in schema and len(instance) < schema['minLength']:
            errors.append('%s: shorter than minLength %d' % (path, schema['minLength']))
        if 'maxLength' in schema and len(instance) > schema['maxLength']:
            errors.append('%s: longer than maxLength %d' % (path, schema['maxLength']))
        if schema.get('format') == 'date' and not _valid_date(instance):
            errors.append('%s: invalid date %r' % (path, instance))
        if schema.get('format') == 'date-time' and not _valid_datetime(instance):
            errors.append('%s: invalid date-time %r' % (path, instance))
    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if 'minimum' in schema and instance < schema['minimum']:
            errors.append('%s: %s < minimum %s' % (path, instance, schema['minimum']))
        if 'maximum' in schema and instance > schema['maximum']:
            errors.append('%s: %s > maximum %s' % (path, instance, schema['maximum']))
    if isinstance(instance, list):
        if 'minItems' in schema and len(instance) < schema['minItems']:
            errors.append('%s: fewer than minItems %d' % (path, schema['minItems']))
        if 'maxItems' in schema and len(instance) > schema['maxItems']:
            errors.append('%s: more than maxItems %d' % (path, schema['maxItems']))
        items = schema.get('items')
        if items is not None:
            for i, item in enumerate(instance):
                if isinstance(items, list):
                    if i < len(items):
                        validate(item, items[i], '%s[%d]' % (path, i), errors)
                else:
                    validate(item, items, '%s[%d]' % (path, i), errors)
    if isinstance(instance, dict):
        props = schema.get('properties', {})
        for key, sub in props.items():
            if key in instance:
                validate(instance[key], sub, '%s.%s' % (path, key), errors)
        for req in schema.get('required', []):
            if req not in instance:
                errors.append('%s: missing required property %r' % (path, req))
        ap = schema.get('additionalProperties')
        if ap is False:
            for key in instance:
                if key not in props:
                    errors.append('%s: unexpected property %r' % (path, key))
        elif isinstance(ap, dict):
            for key, value in instance.items():
                if key not in props:
                    validate(value, ap, '%s.%s' % (path, key), errors)
    return errors
