#!/usr/bin/env python3
"""Validate a journey root against the committed schemas.

Usage: python tools/validate-journey.py [journey-root]
Default root: .journey/  (override to validate a test journey, e.g. workspace/dryrun-journey)
Exit 0 = clean."""

import json
import sys
from pathlib import Path

from _jsonschema_mini import validate as validate_schema

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = ROOT / 'journey' / 'schema'


def load_schema(name):
    return json.loads((SCHEMAS / name).read_text(encoding='utf-8'))


def main():
    journey = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / '.journey'
    if not journey.exists():
        print('journey root not found: %s' % journey)
        sys.exit(1)
    errors = []
    files = 0
    lines = 0

    if (journey / 'profile.json').exists():
        files += 1
        schema = load_schema('profile.schema.json')
        data = json.loads((journey / 'profile.json').read_text(encoding='utf-8'))
        errors += ['profile.json: %s' % e for e in validate_schema(data, schema)]

    for state_name, schema_name in (('skill-matrix.json', 'skill-matrix.schema.json'),
                                    ('review-queue.json', 'review-queue.schema.json'),
                                    ('calibration.json', 'calibration.schema.json')):
        p = journey / 'state' / state_name
        if p.exists():
            files += 1
            schema = load_schema(schema_name)
            data = json.loads(p.read_text(encoding='utf-8'))
            errors += ['state/%s: %s' % (state_name, e) for e in validate_schema(data, schema)]

    event_schema = load_schema('event.schema.json')
    for log in sorted((journey / 'logs').glob('*.jsonl')) if (journey / 'logs').exists() else []:
        files += 1
        for lineno, line in enumerate(log.read_text(encoding='utf-8').splitlines(), 1):
            if not line.strip():
                continue
            lines += 1
            try:
                data = json.loads(line)
            except ValueError as exc:
                errors.append('%s:%d: invalid JSON: %s' % (log.name, lineno, exc))
                continue
            errors += ['%s:%d: %s' % (log.name, lineno, e) for e in validate_schema(data, event_schema)]

    for e in errors:
        print('ERROR: %s' % e)
    print('validate-journey: %d files, %d log lines, %d error(s)' % (files, lines, len(errors)))
    sys.exit(1 if errors else 0)


if __name__ == '__main__':
    main()
