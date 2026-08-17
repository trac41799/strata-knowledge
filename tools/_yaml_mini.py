#!/usr/bin/env python3
"""Restricted YAML-subset parser for Strata frontmatter and registry files.

Supported: flat `key: value` mappings, quoted/bare scalars, ints, floats,
booleans, null, flow arrays `[a, b]`, and block arrays (`key:` then `- item`
lines). Rejected by design: nested mappings, anchors, aliases, multi-line
strings, inline comments. This is an enforced convention, not a YAML parser.
"""

import re

_NUMBER = re.compile(r'^-?\d+$|^-?\d*\.\d+$')


def parse_scalar(raw):
    v = raw.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"":
        return v[1:-1]
    if v == '':
        return None
    if v.lower() in ('true', 'false'):
        return v.lower() == 'true'
    if v.lower() in ('null', '~'):
        return None
    if _NUMBER.match(v):
        try:
            return int(v)
        except ValueError:
            return float(v)
    if v.startswith('[') and v.endswith(']'):
        inner = v[1:-1].strip()
        if not inner:
            return []
        return [parse_scalar(x) for x in inner.split(',')]
    return v


def parse(text):
    data = {}
    pending_key = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.startswith('#'):
            continue
        if pending_key is not None:
            if line.startswith('- '):
                data.setdefault(pending_key, []).append(parse_scalar(line[2:]))
                continue
            pending_key = None
        m = re.match(r'^([A-Za-z0-9_.\-]+):\s*(.*)$', line)
        if not m:
            raise ValueError('unsupported YAML line: %r' % line)
        key, val = m.group(1), m.group(2).strip()
        if val == '':
            pending_key = key
            data.setdefault(key, [])
        else:
            data[key] = parse_scalar(val)
    return data


def parse_frontmatter(text):
    if not text.startswith('---\n'):
        return None, text
    end = text.find('\n---')
    if end == -1:
        raise ValueError('unterminated frontmatter block')
    return parse(text[4:end]), text[end + 4:]


def dump(data):
    """Deterministic emitter for the same subset (used by generated files)."""
    out = []
    for key in sorted(data):
        out.append('%s: %s' % (key, _dump_value(data[key])))
    return '\n'.join(out) + '\n'


def _dump_value(v):
    if isinstance(v, list):
        return '[%s]' % ', '.join(_dump_scalar(x) for x in v)
    return _dump_scalar(v)


def _dump_scalar(v):
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if v is None:
        return 'null'
    if isinstance(v, (int, float)):
        return str(v)
    return v
