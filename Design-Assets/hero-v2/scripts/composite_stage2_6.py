"""Hero v2 — Stage 2.6: composite the light review frames onto the page token.

    python Design-Assets/hero-v2/scripts/composite_stage2_6.py \
      --renders Design-Assets/hero-v2/renders/stage2_6

Why this step exists: the light review page is a flat near-white field, and Cycles'
denoiser overshoots a flat field (world camera-rays have zero variance, so every
deviation from the page value is denoiser error). Rendered directly, the light
frames carried isolated 255 pixels - 0.012% of the frame - which the card forbids
under "no clipping / blown highlights". Compositing the page under the alpha frame
is the same pattern Stage 1 used for its page-canvas previews, and it lands the page
on the token exactly while leaving the rendered pixels untouched.

The alpha frame is the source of truth for the nodes; this script only supplies the
background. It writes the two light review frames and reports what it measured.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

# The plan's Light page canvas (HERO_PRODUCTION_PLAN_v2.md section 3), which is also
# --color-canvas in src/styles/tokens.css.
PAGE_LIGHT = (0xF7, 0xF8, 0xF5)

# label -> (alpha source, page colour)
JOBS = {
    "02-desktop-light": "12-desktop-light-alpha",
    "04-mobile-light": "14-mobile-light-alpha",
}


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--renders", required=True)
    parser.add_argument("--page", default="f7f8f5")
    parser.add_argument("--report", default=None)
    return parser.parse_args(argv)


def main(argv):
    try:
        from PIL import Image
    except ImportError:                                  # pragma: no cover
        print("composite_stage2_6: Pillow is required (system python)", flush=True)
        return 2
    args = parse_args(argv)
    page = tuple(int(args.page[index:index + 2], 16) for index in (0, 2, 4))
    results = {}
    for label, source in JOBS.items():
        source_path = os.path.join(args.renders, "%s.png" % source)
        target_path = os.path.join(args.renders, "%s.png" % label)
        if not os.path.exists(source_path):
            print("composite_stage2_6: missing %s" % source_path, flush=True)
            return 1
        foreground = Image.open(source_path).convert("RGBA")
        background = Image.new("RGB", foreground.size, page)
        background.paste(foreground, (0, 0), foreground)
        background.save(target_path, format="PNG", optimize=False)

        # Measure what was written: the page must be exactly the token and nothing
        # may sit at or above 254, which is the whole point of compositing.
        pixels = list(background.getdata())
        corner = background.getpixel((2, 2))
        levels = [0.2126 * r + 0.7152 * g + 0.0722 * b for r, g, b in pixels]
        max_level = round(max(levels))
        clipped = sum(1 for value in levels if value >= 254.0)
        corner_level = round(0.2126 * corner[0] + 0.7152 * corner[1] + 0.0722 * corner[2])
        results[label] = dict(
            source=os.path.basename(source_path), target=target_path,
            size=list(background.size), page_rgb=list(page),
            corner_level=corner_level, max_level=max_level,
            clipped_pixels=clipped,
            clipped_pct=round(100.0 * clipped / max(1, len(levels)), 5),
            bytes=os.path.getsize(target_path))
        print("composite_stage2_6: %s from %s -> corner=%d max=%d clipped=%d"
              % (label, source, corner_level, max_level, clipped), flush=True)
    if args.report:
        with open(args.report, "w", encoding="utf-8") as handle:
            json.dump(dict(page=list(page), jobs=results), handle, indent=2,
                      sort_keys=True)
        print("composite_stage2_6: wrote %s" % args.report, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
