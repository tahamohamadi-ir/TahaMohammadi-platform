"""Stage 4.2 — build one candidate (or the production derivative) with the curve delta applied.

Runs inside Blender:

    blender --background --python build_hero_v2_stage4_2.py -- \
        --candidate B --out <dir> [--quick] [--samples 48]

    # production run for the winning candidate, writing the derivative source:
    blender --background --python build_hero_v2_stage4_2.py -- \
        --candidate B --production --root ../..

Everything except the relation stroke weight and its per-theme contrast gain is the approved Stage 3
builder: geometry, animation, cameras, sampling, denoise, alpha handling and theme logic all run
through `build_hero_v2_stage3.main`.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import hero_v2_stage4_2 as s42  # noqa: E402
import build_hero_v2_stage3 as s3  # noqa: E402


def parse(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--candidate', required=True, choices=s42.ORDER)
    parser.add_argument('--out', required=True, help='candidate output directory')
    parser.add_argument('--root', default=None, help='hero-v2 root (production runs)')
    parser.add_argument('--production', action='store_true')
    parser.add_argument('--quick', action='store_true')
    parser.add_argument('--samples', type=int, default=None)
    parser.add_argument('--skip-renders', action='store_true')
    return parser.parse_args(argv)


def main(argv):
    args = parse(argv)
    root = os.path.abspath(args.root or os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    record = s42.apply_overrides(args.candidate)

    out_dir = os.path.abspath(args.out)
    os.makedirs(out_dir, exist_ok=True)

    if args.production:
        blend_out = os.path.join(root, 'source', 'hero-v2-stage4_2.blend')
        renders = os.path.join(root, 'renders', 'stage4_2')
        report = os.path.join(root, 'validation', 'hero-v2-stage4_2-report.json')
    else:
        blend_out = os.path.join(out_dir, f'hero-v2-stage4_2-{args.candidate}.blend')
        renders = os.path.join(out_dir, 'renders')
        report = os.path.join(out_dir, f'{args.candidate}-build-report.json')

    os.makedirs(os.path.dirname(report), exist_ok=True)

    builder_argv = [
        '--blend-out', blend_out,
        '--renders', renders,
        '--report', report,
        '--pivot-scale', '0.20',
    ]
    if args.quick:
        builder_argv.append('--quick')
    if args.skip_renders:
        builder_argv.append('--skip-renders')
    if args.samples:
        builder_argv += ['--samples', str(args.samples)]

    print(f'[stage4.2] candidate {args.candidate}: {json.dumps(record)}')
    print(f'[stage4.2] builder argv: {builder_argv}')

    s3.main(builder_argv)

    record.update({
        'blend_out': os.path.relpath(blend_out, root).replace('\\', '/'),
        'renders': os.path.relpath(renders, root).replace('\\', '/'),
        'report': os.path.relpath(report, root).replace('\\', '/'),
        'quick': bool(args.quick),
        'samples': args.samples,
    })
    with open(os.path.join(out_dir, 'override-record.json'), 'w', encoding='utf-8') as handle:
        json.dump(record, handle, indent=2)
    print(f'[stage4.2] candidate {args.candidate} done: {json.dumps(record)}')


if __name__ == '__main__':
    main(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else [])
