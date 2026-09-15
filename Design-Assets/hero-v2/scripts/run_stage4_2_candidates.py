"""Stage 4.2 — candidate driver (plain Python, no bpy).

Runs one Blender process per candidate so no scene state can leak between them, verifies the frozen
stage sources by hash before and after, and writes a manifest for the delivered-scale evaluation.

    python scripts/run_stage4_2_candidates.py [--samples 48] [--quick] [--only B]

Frozen-stage hashes are asserted, not assumed: earlier stages must stay byte-for-byte identical.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
BLENDER = os.environ.get(
    'HERO_V2_BLENDER',
    r'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe',
)

# Recorded at the start of Stage 4.2; the pass must not move them.
FROZEN = {
    'source/hero-v2-stage3.blend': '7ba69d2e1cf16696f556aa6372be1a5822a61b130551b70ea6eb63d70660d2c2',
    'source/hero-v2-stage2_7.blend': '78d74e51ad428430be32d49aa495b260a9dbe794c32dd49fc66a8177a18b1a31',
    'source/hero-v2-stage2_6.blend': 'd5d7ae75f2dacc62ba921bad5dbc0eb70e3c7a0c9c030c1fe9bbe4cb76c6d1a3',
}
CANDIDATES = ('A', 'B', 'C')


def sha256(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b''):
            digest.update(chunk)
    return digest.hexdigest()


def check_frozen(label):
    """Return the verification block, raising if a frozen stage moved."""
    rows = {}
    for rel, expected in FROZEN.items():
        actual = sha256(os.path.join(ROOT, rel))
        rows[rel] = {'expected': expected, 'actual': actual, 'ok': actual == expected}
        if actual != expected:
            raise SystemExit(f'[{label}] frozen stage changed: {rel}\n  expected {expected}\n  actual   {actual}')
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--samples', type=int, default=48, help='quick samples for candidates')
    parser.add_argument('--quick', action='store_true', default=True)
    parser.add_argument('--skip-renders', action='store_true')
    parser.add_argument('--only', default=None, help='run a single candidate letter')
    args = parser.parse_args()

    candidates = (args.only,) if args.only else CANDIDATES
    out_root = os.path.join(ROOT, 'renders', 'stage4_2', 'candidates')
    os.makedirs(out_root, exist_ok=True)

    before = check_frozen('before')
    manifest = {'frozen_before': before, 'candidates': {}, 'blender': BLENDER}

    for candidate in candidates:
        out_dir = os.path.join(out_root, candidate)
        command = [
            BLENDER, '--background', '--python',
            os.path.join(ROOT, 'scripts', 'build_hero_v2_stage4_2.py'), '--',
            '--candidate', candidate,
            '--out', out_dir,
            '--samples', str(args.samples),
        ]
        if args.quick:
            command.append('--quick')
        if args.skip_renders:
            command.append('--skip-renders')

        print(f'[driver] candidate {candidate}: {" ".join(command)}', flush=True)
        result = subprocess.run(command, capture_output=True, text=True)
        log_path = os.path.join(out_dir, 'blender.log')
        os.makedirs(out_dir, exist_ok=True)
        with open(log_path, 'w', encoding='utf-8') as handle:
            handle.write(result.stdout + '\n--- stderr ---\n' + result.stderr)

        record_path = os.path.join(out_dir, 'override-record.json')
        record = json.load(open(record_path, encoding='utf-8')) if os.path.exists(record_path) else None
        renders = sorted(
            os.path.relpath(os.path.join(base, name), ROOT).replace('\\', '/')
            for base, _, names in os.walk(os.path.join(out_dir, 'renders'))
            for name in names
            if name.lower().endswith('.png')
        )
        manifest['candidates'][candidate] = {
            'exit_code': result.returncode,
            'override': record,
            'render_count': len(renders),
            'renders': renders,
            'log': os.path.relpath(log_path, ROOT).replace('\\', '/'),
        }
        print(f'[driver] candidate {candidate}: exit={result.returncode} renders={len(renders)}', flush=True)
        if result.returncode != 0:
            print(result.stdout[-2000:], flush=True)
            print(result.stderr[-2000:], flush=True)

    manifest['frozen_after'] = check_frozen('after')
    manifest_path = os.path.join(out_root, 'manifest.json')
    with open(manifest_path, 'w', encoding='utf-8') as handle:
        json.dump(manifest, handle, indent=2)
    print(f'[driver] manifest: {manifest_path}', flush=True)


if __name__ == '__main__':
    main()
