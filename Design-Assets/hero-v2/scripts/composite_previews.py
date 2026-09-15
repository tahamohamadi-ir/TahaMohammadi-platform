# composite_previews.py -- put the transparent graybox renders on the real page
# canvas, and measure how well the forms actually separate from it.
#
# Why this is a separate step: Blender renders the plan's transparent film RGBA
# PNGs, but its bundled Python has no Pillow. Compositing here, with the system
# Python, is also the more honest preview -- `Image.composite` performs exactly
# `fg*a + bg*(1-a)` on the sRGB bytes, which is what a browser does when it lays
# a translucent image over the page background.
#
# The metrics matter as much as the composite: "reads as premium" is a claim, so
# this reports the measured tonal distance between the forms and the page. A
# form median only ~25 levels below a 247 background is invisible at page size,
# and that is exactly the failure a graybox review has to catch early.
#
# Usage:
#   python composite_previews.py --renders <dir> [--hex "#f7f8f5"]
#                                 [--suffix -alpha] [--keys desktop,mobile]
#                                 [--metrics <json>] [--min-delta 45]
import argparse
import json
import os
import sys

try:
    from PIL import Image
except ImportError:  # pragma: no cover - environment guard
    print("FAIL: Pillow is required (pip install pillow)", file=sys.stderr)
    raise SystemExit(2)


def hex_to_rgb(value):
    h = value.lstrip("#")
    if len(h) != 6:
        raise ValueError("expected a 6-digit hex colour, got %r" % value)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def composite(src, dest, canvas_rgb):
    with Image.open(src) as handle:
        fg = handle.convert("RGBA")
    background = Image.new("RGB", fg.size, canvas_rgb)
    out = Image.composite(fg.convert("RGB"), background, fg.getchannel("A"))
    os.makedirs(os.path.dirname(os.path.abspath(dest)), exist_ok=True)
    out.save(dest, "PNG", optimize=True)
    return fg, os.path.getsize(dest)


def tonal_metrics(fg, canvas_rgb):
    """Luminance distribution over the FORM pixels only (alpha > 200)."""
    import numpy as np

    arr = np.asarray(fg.convert("RGBA")).astype(np.int16)
    mask = arr[..., 3] > 200
    if not mask.any():
        return {"form_pixels": 0}
    rgb = arr[..., :3]
    lum = (0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2])
    values = lum[mask]
    background = (0.2126 * canvas_rgb[0] + 0.7152 * canvas_rgb[1]
                  + 0.0722 * canvas_rgb[2])
    near = {str(d): round(100.0 * float(np.mean(np.abs(values - background) <= d)), 2)
            for d in (5, 10, 15, 20)}
    return {
        "form_pixels": int(mask.sum()),
        "background_luma": round(float(background), 1),
        "form_luma": {
            "min": int(values.min()),
            "p5": round(float(np.percentile(values, 5)), 1),
            "median": round(float(np.median(values)), 1),
            "p95": round(float(np.percentile(values, 95)), 1),
            "max": int(values.max()),
            "mean": round(float(values.mean()), 1),
        },
        "median_delta_from_canvas": round(float(background - np.median(values)), 1),
        "pct_form_within_delta": near,
    }


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--renders", required=True)
    parser.add_argument("--hex", default="#f7f8f5")
    parser.add_argument("--suffix", default="-alpha")
    parser.add_argument("--keys", default="desktop,mobile")
    parser.add_argument("--metrics")
    parser.add_argument("--min-delta", type=float, default=45.0,
                        help="minimum acceptable form-median distance from the canvas")
    args = parser.parse_args(argv)

    canvas = hex_to_rgb(args.hex)
    report, failures = {}, 0
    for key in [k.strip() for k in args.keys.split(",") if k.strip()]:
        src = os.path.join(args.renders, "graybox-%s%s.png" % (key, args.suffix))
        dest = os.path.join(args.renders, "graybox-%s.png" % key)
        if not os.path.exists(src):
            print("MISSING %s" % src, file=sys.stderr)
            failures += 1
            continue
        fg, nbytes = composite(src, dest, canvas)
        metrics = tonal_metrics(fg, canvas)
        ok = metrics.get("median_delta_from_canvas", 0.0) >= args.min_delta
        metrics["median_delta_pass"] = ok
        metrics["required_median_delta"] = args.min_delta
        report[key] = metrics
        print("composited %-26s %sx%s -> %s (%d bytes) on %s"
              % (os.path.basename(src), fg.size[0], fg.size[1],
                 os.path.basename(dest), nbytes, args.hex))
        print("   form luma median %s vs canvas %s (delta %s, need >= %s) -> %s"
              % (metrics["form_luma"]["median"], metrics["background_luma"],
                 metrics["median_delta_from_canvas"], args.min_delta,
                 "PASS" if ok else "FAIL"))
        if not ok:
            failures += 1

    if args.metrics:
        os.makedirs(os.path.dirname(os.path.abspath(args.metrics)), exist_ok=True)
        with open(args.metrics, "w", encoding="utf-8") as handle:
            json.dump({"canvas": args.hex, "keys": report}, handle, indent=2,
                      sort_keys=True)
        print("wrote %s" % args.metrics)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
