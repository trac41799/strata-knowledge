#!/usr/bin/env python3
"""Scaffold a new topic pack: knowledge/<track>/<slug>/ concept.md +
validation.md + teaching.md (+ frontier.md with --frontier)."""

import argparse
import sys
from datetime import date
from pathlib import Path

from _yaml_mini import parse as parse_yaml

ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE = ROOT / 'knowledge'
TRACKS_FILE = ROOT / 'tracks.yml'


def main():
    parser = argparse.ArgumentParser(description='Scaffold a Strata topic pack')
    parser.add_argument('--track', required=True, help='track id from tracks.yml')
    parser.add_argument('--slug', required=True, help='topic slug (kebab-case)')
    parser.add_argument('--title', default=None, help='human title (default: slug)')
    parser.add_argument('--band', default='B3', choices=['B0', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6'])
    parser.add_argument('--tier', default='T3', choices=['T0', 'T1', 'T2', 'T3', 'T4'])
    parser.add_argument('--bloom-target', default='apply',
                        choices=['remember', 'understand', 'apply', 'analyze', 'evaluate', 'create'])
    parser.add_argument('--prereqs', default='', help='comma-separated topic ids')
    parser.add_argument('--related', default='', help='comma-separated topic ids')
    parser.add_argument('--owner', default='unassigned', help='owning agent id')
    parser.add_argument('--frontier', action='store_true', help='also create frontier.md (tier T4)')
    args = parser.parse_args()

    tracks_data = parse_yaml(TRACKS_FILE.read_text(encoding='utf-8'))
    tracks = tracks_data.get('tracks', [])
    if args.track not in tracks:
        print('ERROR: track %r not in tracks.yml' % args.track)
        sys.exit(1)
    topic_id = '%s/%s' % (args.track, args.slug)
    folder = KNOWLEDGE / args.track / args.slug
    if folder.exists():
        print('ERROR: topic folder already exists: %s' % folder)
        sys.exit(1)
    folder.mkdir(parents=True)

    prereqs = [p.strip() for p in args.prereqs.split(',') if p.strip()]
    related = [r.strip() for r in args.related.split(',') if r.strip()]
    title = args.title or args.slug
    today = date.today().isoformat()
    fm = [
        '---',
        'id: %s' % topic_id,
        'title: %s' % title,
        'band: %s' % args.band,
        'track: %s' % args.track,
        'tier: %s' % args.tier,
        'bloom_target: %s' % args.bloom_target,
        'prerequisites: [%s]' % ', '.join(prereqs),
        'related: [%s]' % ', '.join(related),
        'status: draft',
        'schema-version: 1',
        'owner: %s' % args.owner,
        'reviewed-by: []',
        'updated: %s' % today,
        'sources: []',
    ]
    if args.tier == 'T4':
        fm.append('review_after: %s' % today)
    fm.append('---')

    concept = fm + [
        '',
        '# %s' % title,
        '',
        '## Claims',
        '',
        '- <Claim sentence, one per bullet, each tagged `[%s]` + `[S-####]`.>' % args.tier,
        '',
        '## Details',
        '',
        '## Boundaries / common misunderstandings',
        '',
        '## References (evidence records)',
        '',
        '- `S-####` — <source short description>',
    ]
    validation = fm + [
        '',
        '# %s — validation' % title,
        '',
        '## Formative (practice)',
        '',
        '- Q: <question>',
        '- bloom: understand',
        '- bank: formative',
        '- A: <model answer>',
        '- evidence: [S-####]',
        '',
        '## Summative (mastery checkpoint)',
        '',
        '- Q: <question at bloom_target level>',
        '- bloom: %s' % args.bloom_target,
        '- bank: summative',
        '- A: <model answer>',
        '- evidence: [S-####]',
        '',
        '## Review (spaced repetition — interleaved with prerequisites)',
        '',
        '- Q: <question>',
        '- bloom: remember',
        '- bank: review',
        '- A: <model answer>',
        '- evidence: [S-####]',
    ]
    teaching = fm + [
        '',
        '# %s — teaching' % title,
        '',
        '## Learning objectives (Bloom)',
        '',
        '- Understand: <objective>',
        '- %s: <objective>' % args.bloom_target.capitalize(),
        '',
        '## Worked example',
        '',
        '## Elaboration prompts (why does X work?)',
        '',
        '## Common misconceptions (3+)',
        '',
        '## Feynman targets (explain-back checkpoints)',
        '',
        '## Interleaving hooks (prerequisites to mix in)',
    ]

    (folder / 'concept.md').write_text('\n'.join(concept) + '\n', encoding='utf-8')
    (folder / 'validation.md').write_text('\n'.join(validation) + '\n', encoding='utf-8')
    (folder / 'teaching.md').write_text('\n'.join(teaching) + '\n', encoding='utf-8')
    if args.frontier or args.tier == 'T4':
        (folder / 'frontier.md').write_text('\n'.join(fm + ['', '# %s — frontier notes' % title, '',
                                                            'Volatile, tier T4. Review by %s.' % today]) + '\n',
                                            encoding='utf-8')
    print('created topic pack: %s' % topic_id)
    print('next: fill content, then run: python tools/lint.py && python tools/check-graph.py')


if __name__ == '__main__':
    main()
