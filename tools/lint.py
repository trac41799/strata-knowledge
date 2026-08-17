#!/usr/bin/env python3
"""Strata linter: frontmatter schema, claim->evidence integrity, links,
T4/staleness rules, journey examples. Exit 0 = clean."""

import json
import re
import sys
from datetime import date
from pathlib import Path

from _jsonschema_mini import validate as validate_schema
from _yaml_mini import parse as parse_yaml
from _yaml_mini import parse_frontmatter

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = ROOT / 'tools' / 'schemas'
EVIDENCE_DIR = ROOT / 'evidence' / 'records'
KNOWLEDGE = ROOT / 'knowledge'
JOURNEY = ROOT / 'journey'
TRACKS_FILE = ROOT / 'tracks.yml'
TODAY = date.today()

ERRORS = []
WARNINGS = []


def error(msg):
    ERRORS.append(msg)


def warning(msg):
    WARNINGS.append(msg)


def load_json(path):
    with open(path, encoding='utf-8') as fh:
        return json.load(fh)


def load_schema(name):
    return load_json(SCHEMA_DIR / name)


def months_before_today(n):
    year = TODAY.year
    month = TODAY.month - n
    while month <= 0:
        month += 12
        year -= 1
    return date(year, month, TODAY.day)


TOPIC_SCHEMA = load_schema('topic.schema.json')
EVIDENCE_SCHEMA = load_schema('evidence.schema.json')
TIER_TAG = re.compile(r'\[T[0-4]\]')
RECORD_REF = re.compile(r'\bS-\d{4}\b')
LINK_REF = re.compile(r'\[[^\]]*\]\(([^)]+)\)')
TRAILING_HASH = re.compile(r'#.*$')


def check_tracks_file():
    if not TRACKS_FILE.exists():
        error('tracks.yml missing')
        return None
    try:
        data = parse_yaml(TRACKS_FILE.read_text(encoding='utf-8'))
    except ValueError as exc:
        error('tracks.yml unparseable: %s' % exc)
        return None
    tracks = data.get('tracks')
    if not isinstance(tracks, list) or not tracks:
        error('tracks.yml: "tracks" list missing or empty')
        return None
    return tracks


TRACKS = check_tracks_file()


def check_frontmatter(path, schema, kind):
    text = path.read_text(encoding='utf-8')
    try:
        fm, _ = parse_frontmatter(text)
    except ValueError as exc:
        error('%s: %s' % (path, exc))
        return None
    if fm is None:
        error('%s: missing frontmatter (required for %s files)' % (path, kind))
        return None
    errs = validate_schema(fm, schema)
    for e in errs:
        error('%s: frontmatter %s' % (path, e))
    return fm


def check_topic_file(path, expected_id, is_concept):
    fm = check_frontmatter(path, TOPIC_SCHEMA, 'topic')
    if fm is None:
        return
    if fm.get('id') != expected_id:
        error('%s: frontmatter id %r does not match folder path %r' % (path, fm.get('id'), expected_id))
    track = fm.get('track')
    if TRACKS and track not in TRACKS:
        error('%s: track %r not in tracks.yml' % (path, track))
    status = fm.get('status')
    if status in ('validated', 'published') and not fm.get('reviewed-by'):
        error('%s: status %s requires non-empty reviewed-by' % (path, status))
    if status == 'published' and not fm.get('sources'):
        error('%s: status published requires non-empty sources' % (path))
    tier = fm.get('tier')
    if tier == 'T4':
        if not fm.get('review_after'):
            error('%s: tier T4 requires review_after date' % path)
        elif fm['review_after'] < TODAY.isoformat():
            error('%s: review_after %s is expired (tier T4 content must be re-reviewed)' % (path, fm['review_after']))
    updated = fm.get('updated')
    if updated:
        try:
            if date.fromisoformat(updated) < months_before_today(18):
                error('%s: content stale (updated %s > 18 months ago)' % (path, updated))
        except ValueError:
            error('%s: invalid updated date %r' % (path, updated))
    for rid in fm.get('sources', []):
        if not (EVIDENCE_DIR / ('%s.md' % rid)).exists():
            error('%s: sources references missing record %s' % (path, rid))
    if is_concept:
        check_claim_evidence(path, fm)
    check_links(path)


def check_claim_evidence(path, fm):
    lines = path.read_text(encoding='utf-8').splitlines()
    for i, line in enumerate(lines, 1):
        if TIER_TAG.search(line):
            if not RECORD_REF.search(line):
                error('%s:%d: claim tag %r without an S-#### record reference' % (path, i, TIER_TAG.search(line).group(0)))
        for m in RECORD_REF.finditer(line):
            rid = m.group(0)
            if not (EVIDENCE_DIR / ('%s.md' % rid)).exists():
                error('%s:%d: record %s referenced but missing' % (path, i, rid))
    tier = fm.get('tier')
    if tier is None:
        return
    tag = '[T%s]' % tier[1]
    if tag not in path.read_text(encoding='utf-8'):
        warning('%s: frontmatter tier %s has no matching %s tag in body' % (path, tier, tag))


def check_links(path):
    text = path.read_text(encoding='utf-8')
    for m in LINK_REF.finditer(text):
        target = m.group(1)
        if '://' in target or target.startswith('#') or target.startswith('mailto:'):
            continue
        target = TRAILING_HASH.sub('', target)
        if not target or target.endswith(('.png', '.jpg', '.gif', '.svg')):
            continue
        resolved = (path.parent / target).resolve()
        if not resolved.exists():
            error('%s: broken link -> %s' % (path, target))


def check_topic_folders():
    if not KNOWLEDGE.exists():
        return
    for concept in sorted(KNOWLEDGE.rglob('concept.md')):
        rel = concept.relative_to(KNOWLEDGE)
        if len(rel.parts) != 3 or rel.parts[-1] != 'concept.md':
            error('%s: topic folders must be exactly <track>/<topic>/concept.md' % concept)
            continue
        expected_id = '%s/%s' % (rel.parts[0], rel.parts[1])
        check_topic_file(concept, expected_id, True)
        folder = concept.parent
        has_validation = (folder / 'validation.md').exists()
        has_teaching = (folder / 'teaching.md').exists()
        if has_validation:
            check_topic_file(folder / 'validation.md', expected_id, False)
        if has_teaching:
            check_topic_file(folder / 'teaching.md', expected_id, False)
        if (folder / 'frontier.md').exists():
            check_topic_file(folder / 'frontier.md', expected_id, False)
        fm = parse_frontmatter(concept.read_text(encoding='utf-8'))[0] or {}
        status = fm.get('status')
        if status == 'published' and not (has_validation and has_teaching):
            error('%s: status published requires validation.md and teaching.md' % folder)
        if not (has_validation or has_teaching):
            warning('%s: topic lacks validation.md and teaching.md (fine for drafts)' % folder)


def check_evidence_records():
    if not EVIDENCE_DIR.exists():
        return
    for path in sorted(EVIDENCE_DIR.glob('*.md')):
        fm = check_frontmatter(path, EVIDENCE_SCHEMA, 'evidence')
        if fm is None:
            continue
        rid = fm.get('id')
        if rid and path.stem != rid:
            error('%s: filename does not match record id %r' % (path, rid))


def check_journey_examples():
    examples = JOURNEY / 'examples'
    if not examples.exists():
        return
    for path in sorted(examples.iterdir()):
        stem = path.stem
        schema_stem = stem.replace('.example', '') + '.schema.json'
        schema_path = JOURNEY / 'schema' / schema_stem
        if not schema_path.exists():
            error('%s: no matching journey schema %s' % (path, schema_path.name))
            continue
        schema = load_json(schema_path)
        if path.suffix == '.json':
            try:
                data = json.loads(path.read_text(encoding='utf-8'))
            except ValueError as exc:
                error('%s: invalid JSON: %s' % (path, exc))
                continue
            errs = validate_schema(data, schema)
            for e in errs:
                error('%s: %s' % (path, e))
        elif path.suffix == '.jsonl':
            event_schema = load_json(JOURNEY / 'schema' / 'event.schema.json')
            for lineno, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                except ValueError as exc:
                    error('%s:%d: invalid JSON: %s' % (path, lineno, exc))
                    continue
                errs = validate_schema(data, event_schema)
                for e in errs:
                    error('%s:%d: %s' % (path, lineno, e))


def main():
    check_topic_folders()
    check_evidence_records()
    check_journey_examples()
    for w in WARNINGS:
        print('WARN: %s' % w)
    for e in ERRORS:
        print('ERROR: %s' % e)
    if ERRORS:
        print('lint failed: %d error(s)' % len(ERRORS))
        sys.exit(1)
    print('lint OK (%d warning(s))' % len(WARNINGS))


if __name__ == '__main__':
    main()
