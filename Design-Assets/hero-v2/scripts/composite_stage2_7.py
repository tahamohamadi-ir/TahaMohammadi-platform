"""Hero v2 — Stage 2.7: composite the light page and make the web-scale previews.

    python Design-Assets/hero-v2/scripts/composite_stage2_7.py \
      --renders Design-Assets/hero-v2/renders/stage2_7

Two jobs, both of which the card asks for explicitly:

1. **Light review frames** (`02-`, `04-`) are the alpha frame composited onto the
   page token. Rendering a flat near-white page directly is what the Stage 2.6
   denoiser overshoot punished; compositing lands the page on `#f7f8f5` exactly and
   keeps every pixel below 255.
2. **Web-scale previews** (`21-`..`24-`) downsample the review frames to the real CSS
   footprint - desktop 686x600, mobile 288x288, from the plan's 600 px and 288 px slot
   heights. These exist so the look is judged at the size it will actually be seen
   rather than only at 1600x1400, which is where edge thickness and texture survival
   have to be checked.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from PIL import Image, ImageChops

PAGE_LIGHT = (0xF7, 0xF8, 0xF5)
LIGHT_JOBS = {"02-desktop-light": "12-desktop-light-alpha",
              "04-mobile-light": "14-mobile-light-alpha"}
WEBSCALE = {"21-desktop-dark-webscale": ("01-desktop-dark", (686, 600)),
            "22-desktop-light-webscale": ("02-desktop-light", (686, 600)),
            "23-mobile-dark-webscale": ("03-mobile-dark", (288, 288)),
            "24-mobile-light-webscale": ("04-mobile-light", (288, 288))}


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--renders", required=True)
    parser.add_argument("--page", default="f7f8f5")
    parser.add_argument("--report", default=None)
    return parser.parse_args(argv)


def luminance(red, green, blue):
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def main(argv):
    try:
        from PIL import Image
    except ImportError:                                  # pragma: no cover
        print("composite_stage2_7: Pillow is required (system python)", flush=True)
        return 2
    args = parse_args(argv)
    page = tuple(int(args.page[index:index + 2], 16) for index in (0, 2, 4))
    results = {}

    for label, source in LIGHT_JOBS.items():
        source_path = os.path.join(args.renders, "%s.png" % source)
        target_path = os.path.join(args.renders, "%s.png" % label)
        if not os.path.exists(source_path):
            print("composite_stage2_7: missing %s" % source_path, flush=True)
            return 1
        foreground = Image.open(source_path).convert("RGBA")
        background = Image.new("RGB", foreground.size, page)
        background.paste(foreground, (0, 0), foreground)
        background.save(target_path, format="PNG")

        pixels = list(background.getdata())
        levels = [luminance(*pixel) for pixel in pixels]
        corner = background.getpixel((2, 2))
        clipped = sum(1 for value in levels if value >= 254.0)
        results[label] = dict(kind="light_page_composite",
                              source=os.path.basename(source_path),
                              size=list(background.size),
                              corner_level=round(luminance(*corner)),
                              max_level=round(max(levels)), clipped_pixels=clipped,
                              bytes=os.path.getsize(target_path))
        print("composite_stage2_7: %s <- %s corner=%d max=%d clipped=%d"
              % (label, source, results[label]["corner_level"],
                 results[label]["max_level"], clipped), flush=True)

    for label, (source, size) in WEBSCALE.items():
        source_path = os.path.join(args.renders, "%s.png" % source)
        target_path = os.path.join(args.renders, "%s.png" % label)
        if not os.path.exists(source_path):
            print("composite_stage2_7: missing %s" % source_path, flush=True)
            return 1
        frame = Image.open(source_path).convert("RGB")
        preview = frame.resize(size, Image.LANCZOS)
        # LANCZOS rings: a sharp dark edge against a 248 field overshoots past the
        # page and pokes pixels at 255 (measured 223 of them in the light preview,
        # from a source frame with none). Clamping to the source's own maximum keeps
        # the resampling sharp without inventing values the render never had.
        source_max = max(frame.getextrema(), key=lambda pair: pair[1])[1]
        clamp = Image.new("RGB", preview.size, (source_max, source_max, source_max))
        preview = ImageChops.darker(preview, clamp)
        preview.save(target_path, format="PNG")
        levels = [luminance(*pixel) for pixel in preview.getdata()]
        results[label] = dict(kind="webscale_preview", source=os.path.basename(source_path),
                              source_size=list(frame.size), size=list(preview.size),
                              source_max=source_max,
                              max_level=round(max(levels)),
                              clipped_pixels=sum(1 for value in levels if value >= 254.0),
                              bytes=os.path.getsize(target_path))
        print("composite_stage2_7: %s <- %s at %s (max=%d clipped=%d)"
              % (label, source, size, results[label]["max_level"],
                 results[label]["clipped_pixels"]), flush=True)

    if args.report:
        with open(args.report, "w", encoding="utf-8") as handle:
            json.dump(dict(page=list(page), jobs=results), handle, indent=2,
                      sort_keys=True)
        print("composite_stage2_7: wrote %s" % args.report, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
