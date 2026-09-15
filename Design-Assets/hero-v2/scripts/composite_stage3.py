"""Hero v2 — Stage 3: composite the light review frames onto the light page.

    python Design-Assets/hero-v2/scripts/composite_stage3.py \
      --renders Design-Assets/hero-v2/renders/stage3

Stage 2.7 established why this is a separate Pillow step: a flat near-white page is exactly
what Cycles' denoiser overshoots, so the alpha masters are the source of truth and the page
is composited under them with the browser's own arithmetic (`fg*a + bg*(1-a)` on sRGB bytes).
Stage 3 needs it eight times (two devices x four states, light theme only).

The dark review frames are rendered opaque by the builder - they carry the navy gradient
world, which no flat composite can reproduce - so nothing here touches them.
"""

from __future__ import annotations

import argparse
import json
import os

from PIL import Image, ImageStat

PAGE_LIGHT = (0xF7, 0xF8, 0xF5)
STATES = ("01", "02", "03", "04")
JOBS = tuple(("%s/light/frame-%s" % (device, index),
              "alpha/%s-light-%s" % (device, index))
             for device in ("desktop", "mobile") for index in STATES)


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--renders", required=True)
    parser.add_argument("--report", default=None)
    return parser.parse_args(argv)


def compose(alpha_path, page):
    image = Image.open(alpha_path).convert("RGBA")
    background = Image.new("RGBA", image.size, page + (255,))
    return Image.alpha_composite(background, image).convert("RGB")


def main(argv):
    args = parse_args(argv)
    root = os.path.abspath(args.renders)
    report = {}
    for label, source in JOBS:
        target = os.path.join(root, "%s.png" % label)
        alpha = os.path.join(root, "%s.png" % source)
        if not os.path.exists(alpha):
            report[label] = dict(skipped="missing %s" % source)
            continue
        image = compose(alpha, PAGE_LIGHT)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        image.save(target)
        grey = image.convert("L")
        histogram = grey.histogram()
        report[label] = dict(
            from_alpha=source, bytes=os.path.getsize(target),
            size=list(image.size), page_level=round(sum(PAGE_LIGHT) / 3.0, 1),
            max_level=int(ImageStat.Stat(grey).extrema[0][1]),
            clipped_pixels=sum(histogram[254:]))
    if args.report:
        os.makedirs(os.path.dirname(os.path.abspath(args.report)), exist_ok=True)
        with open(args.report, "w", encoding="utf-8") as handle:
            json.dump(dict(jobs=report), handle, indent=2, sort_keys=True)
    for label, entry in sorted(report.items()):
        print("%-28s %s" % (label, json.dumps(entry)))
    return report


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
