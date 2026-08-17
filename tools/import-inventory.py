#!/usr/bin/env python3
"""Bulk-scaffold topic packs from docs/topic-inventory.yml (Phase 1.4).

Creates knowledge/<track>/<slug>/{concept,validation,teaching}.md with valid
frontmatter and empty sections (no claim tags -> lint-safe drafts).
Fails if any target folder already exists. T4 topics get review_after = today + 183 days."""

import sys
from datetime import date, timedelta
from pathlib import Path

from _yaml_mini import parse as parse_yaml

ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE = ROOT / 'knowledge'
MANIFEST = ROOT / 'docs' / 'topic-inventory.yml'

BANDS = ['B0', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6']
TIERS = ['T0', 'T1', 'T2', 'T3', 'T4']
BLOOMS = ['remember', 'understand', 'apply', 'analyze', 'evaluate', 'create']

PREFIX = 'topic.'
FIELDS = ('title', 'band', 'tier', 'bloom', 'prereqs', 'recommended', 'related')


def load_manifest():
    data = parse_yaml(MANIFEST.read_text(encoding='utf-8'))
    topics = {}
    for key, value in data.items():
        if not key.startswith(PREFIX):
            continue
        rest = key[len(PREFIX):]
        parts = rest.split('.')
        if len(parts) != 3:
            print('ERROR: malformed manifest key %r' % key)
            sys.exit(1)
        track, slug, field = parts
        if field not in FIELDS:
            print('ERROR: unknown field %r in %r' % (field, key))
            sys.exit(1)
        topic_id = '%s/%s' % (track, slug)
        topics.setdefault(topic_id, {'track': track, 'slug': slug})[field] = value
    errors = []
    for tid, t in topics.items():
        missing = [f for f in ('title', 'band', 'tier', 'bloom') if t.get(f) is None]
        if missing:
            errors.append('%s: missing fields %s' % (tid, missing))
        if t.get('band') not in BANDS:
            errors.append('%s: invalid band %r' % (tid, t.get('band')))
        if t.get('tier') not in TIERS:
            errors.append('%s: invalid tier %r' % (tid, t.get('tier')))
        if t.get('bloom') not in BLOOMS:
            errors.append('%s: invalid bloom %r' % (tid, t.get('bloom')))
        for lst_field in ('prereqs', 'recommended', 'related'):
            if not isinstance(t.get(lst_field), list):
                errors.append('%s: %s must be a list' % (tid, lst_field))
    for e in errors:
        print('ERROR: %s' % e)
    if errors:
        sys.exit(1)
    return topics


def build_files(t, today):
    tid = '%s/%s' % (t['track'], t['slug'])
    title = t['title']
    review_after = (today + timedelta(days=183)).isoformat()
    today_iso = today.isoformat()
    fm = [
        '---',
        'id: %s' % tid,
        'title: %s' % title,
        'band: %s' % t['band'],
        'track: %s' % t['track'],
        'tier: %s' % t['tier'],
        'bloom_target: %s' % t['bloom'],
        'prerequisites: [%s]' % ', '.join(t.get('prereqs', [])),
        'recommended: [%s]' % ', '.join(t.get('recommended', [])),
        'related: [%s]' % ', '.join(t.get('related', [])),
        'status: draft',
        'schema-version: 1',
        'owner: l0-inventory',
        'reviewed-by: []',
        'updated: %s' % today_iso,
        'sources: []',
    ]
    if t['tier'] == 'T4':
        fm.append('review_after: %s' % review_after)
    fm.append('---')
    concept = fm + [
        '',
        '# %s' % title,
        '',
        '## Claims',
        '',
        '> To be authored in Phase 2/3 by L1 research + L2 validation.',
        '',
        '## Details',
        '',
        '## Boundaries / common misunderstandings',
        '',
        '## References (evidence records)',
    ]
    validation = fm + [
        '',
        '# %s — validation' % title,
        '',
        '## Formative (practice)',
        '',
        '> To be authored by L3 pedagogy.',
        '',
        '## Summative (mastery checkpoint)',
        '',
        '## Review (spaced repetition — interleaved with prerequisites)',
    ]
    teaching = fm + [
        '',
        '# %s — teaching' % title,
        '',
        '## Learning objectives (Bloom)',
        '',
        '> To be authored by L3 pedagogy.',
        '',
        '## Worked example',
        '',
        '## Elaboration prompts',
        '',
        '## Common misconceptions',
        '',
        '## Feynman targets',
        '',
        '## Interleaving hooks',
    ]
    return concept, validation, teaching


def main():
    today = date.today()
    topics = load_manifest()
    created = {}
    for tid in sorted(topics):
        t = topics[tid]
        folder = KNOWLEDGE / t['track'] / t['slug']
        if folder.exists():
            print('ERROR: topic folder already exists: %s' % folder)
            sys.exit(1)
        folder.mkdir(parents=True)
        concept, validation, teaching = build_files(t, today)
        (folder / 'concept.md').write_text('\n'.join(concept) + '\n', encoding='utf-8')
        (folder / 'validation.md').write_text('\n'.join(validation) + '\n', encoding='utf-8')
        (folder / 'teaching.md').write_text('\n'.join(teaching) + '\n', encoding='utf-8')
        created.setdefault(t['track'], []).append(tid)
    for track, ids in sorted(created.items()):
        print('%s: %d topics' % (track, len(ids)))
    print('import OK: %d topics scaffolded' % sum(len(v) for v in created.values()))


if __name__ == '__main__':
    main()
