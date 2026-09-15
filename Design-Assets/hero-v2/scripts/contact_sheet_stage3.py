"""Hero v2 — Stage 3: contact sheets, motion-difference diagnostic, review GIF.

    python Design-Assets/hero-v2/scripts/contact_sheet_stage3.py \
      --renders    Design-Assets/hero-v2/renders/stage3 \
      --validation Design-Assets/hero-v2/validation

Four contact sheets (desktop/mobile x dark/light), each reading 01 -> 02 -> 03 -> 04 side by
side so continuity is judged by the eye and not by the report. Then the motion-difference
diagnostic: consecutive alpha silhouettes differenced and false-coloured, so "the companions
moved through depth" appears as a shape rather than as an assertion. Finally a cross-dissolve
GIF for design review only - not a web asset, nothing downstream reads it.

Silhouette metric, used here for the sheet and independently in the validator for the
continuity test: mean absolute difference of the alpha channel, and intersection-over-union
of the silhouette thresholded at alpha >= 0.5. The definition is repeated in both files on
purpose; neither imports the other, so a shared bug is not possible.
"""

from __future__ import annotations

import argparse
import json
import os

from PIL import Image, ImageChops, ImageDraw, ImageFont

STATES = ("01", "02", "03", "04")
STEPS = (("01", "02"), ("02", "03"), ("03", "04"), ("01", "04"))
INK = (238, 238, 234)
PAPER = (18, 20, 24)
UNCHANGED = (92, 92, 96)
ONLY_FIRST = (214, 92, 76)
ONLY_SECOND = (74, 138, 196)
LABEL_HEIGHT = 46
PANEL_HEIGHT = 300
DISSOLVE_STEPS = 8
FRAME_MS = 110
GIF_SCALE = 0.42
ALPHA_THRESHOLD = 128


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--renders", required=True)
    parser.add_argument("--validation", required=True)
    parser.add_argument("--report", default=None)
    return parser.parse_args(argv)


def font(size):
    try:
        return ImageFont.truetype("consola.ttf", size)
    except OSError:
        return ImageFont.load_default()


def labelled_strip(panels, captions, header):
    width = sum(panel.width for panel in panels)
    height = max(panel.height for panel in panels) + LABEL_HEIGHT + 34
    sheet = Image.new("RGB", (width, height), PAPER)
    draw = ImageDraw.Draw(sheet)
    draw.text((10, 8), header, fill=INK, font=font(17))
    offset = 0
    for panel, caption in zip(panels, captions):
        sheet.paste(panel, (offset, 32))
        draw.text((offset + 10, 32 + panel.height + 8), caption, fill=INK, font=font(15))
        offset += panel.width
    return sheet


def scaled(path, height):
    image = Image.open(path).convert("RGB")
    ratio = height / float(image.height)
    return image.resize((max(1, int(image.width * ratio)), height), Image.LANCZOS)


def silhouette(path, height):
    """Scaled RGB panel plus its binary silhouette mask."""
    image = Image.open(path).convert("RGBA")
    ratio = height / float(image.height)
    image = image.resize((max(1, int(image.width * ratio)), height), Image.LANCZOS)
    alpha = image.getchannel("A")
    mask = alpha.point(lambda value: 255 if value >= ALPHA_THRESHOLD else 0)
    return image.convert("RGB"), alpha, mask


def difference_panel(mask_first, mask_second):
    """False-coloured displacement: grey unchanged, red leaving, blue arriving."""
    unchanged = ImageChops.darker(mask_first, mask_second)
    only_first = ImageChops.subtract(mask_first, mask_second)
    only_second = ImageChops.subtract(mask_second, mask_first)
    panel = Image.new("RGB", mask_first.size, PAPER)
    for colour, mask in ((UNCHANGED, unchanged), (ONLY_FIRST, only_first),
                         (ONLY_SECOND, only_second)):
        panel.paste(Image.new("RGB", mask_first.size, colour), (0, 0), mask)
    return panel, unchanged, only_first, only_second


def continuity_metrics(alpha_first, alpha_second, mask_first, mask_second):
    common = ImageChops.darker(mask_first, mask_second).histogram()[255]
    pixels_first = mask_first.histogram()[255]
    pixels_second = mask_second.histogram()[255]
    union = pixels_first + pixels_second - common
    difference = ImageChops.difference(alpha_first, alpha_second).histogram()
    mean_delta = sum(index * count for index, count in enumerate(difference)) / float(
        alpha_first.width * alpha_first.height * 255)
    return dict(pixels_first=pixels_first, pixels_second=pixels_second, common=common,
                iou=round(common / float(union), 4) if union else 0.0,
                mean_absolute_alpha_delta=round(mean_delta, 5))


def build_contact_sheets(root, report):
    for device in ("desktop", "mobile"):
        for theme in ("dark", "light"):
            label = "contact-%s-%s" % (device, theme)
            panels = [os.path.join(root, device, theme, "frame-%s.png" % index)
                      for index in STATES]
            if not all(os.path.exists(path) for path in panels):
                report["contact_sheets"][label] = dict(
                    skipped="missing review frames for %s/%s" % (device, theme))
                continue
            sheet = labelled_strip([scaled(path, PANEL_HEIGHT) for path in panels],
                                   ["frame-%s" % index for index in STATES],
                                   "Hero v2 Stage 3 - %s %s - 01 > 02 > 03 > 04"
                                   % (device, theme))
            target = os.path.join(root, "%s.png" % label)
            sheet.save(target)
            report["contact_sheets"][label] = dict(path=target, size=list(sheet.size),
                                                   frames=list(STATES))


def build_diagnostic(root, report):
    for prefix in ("desktop-dark", "mobile-dark"):
        panels, captions, metrics = [], [], {}
        for first, second in STEPS:
            path_first = os.path.join(root, "alpha", "%s-%s.png" % (prefix, first))
            path_second = os.path.join(root, "alpha", "%s-%s.png" % (prefix, second))
            if not (os.path.exists(path_first) and os.path.exists(path_second)):
                metrics = {}
                break
            _rgb_a, alpha_a, mask_a = silhouette(path_first, PANEL_HEIGHT)
            _rgb_b, alpha_b, mask_b = silhouette(path_second, PANEL_HEIGHT)
            panel, _unchanged, _only_first, _only_second = difference_panel(mask_a, mask_b)
            measured = continuity_metrics(alpha_a, alpha_b, mask_a, mask_b)
            metrics["%s->%s" % (first, second)] = measured
            panels.append(panel)
            captions.append("%s -> %s    IoU %.4f    mean|dAlpha| %.5f"
                            % (first, second, measured["iou"],
                               measured["mean_absolute_alpha_delta"]))
        if not panels:
            report["diagnostic"][prefix] = dict(skipped="missing alpha masters")
            continue
        sheet = labelled_strip(panels, captions,
                               "Hero v2 Stage 3 - silhouette displacement (%s) - grey = "
                               "unchanged, red = only the first frame, blue = only the "
                               "second" % prefix)
        target = os.path.join(root, "contact-motion-difference-%s.png" % prefix)
        sheet.save(target)
        report["diagnostic"][prefix] = dict(path=target, size=list(sheet.size),
                                            metrics=metrics)


def build_motion_review(root, validation, report):
    frames = []
    for index in STATES:
        path = os.path.join(root, "desktop", "dark", "frame-%s.png" % index)
        if not os.path.exists(path):
            report["motion_review"] = dict(skipped="missing %s" % path)
            return
        image = Image.open(path).convert("RGB")
        frames.append(image.resize((max(1, int(image.width * GIF_SCALE)),
                                    max(1, int(image.height * GIF_SCALE))), Image.LANCZOS))
    sequence = []
    for position, frame in enumerate(frames):
        following = frames[(position + 1) % len(frames)]
        sequence.append(frame)
        for step in range(1, DISSOLVE_STEPS):
            sequence.append(Image.blend(frame, following, step / float(DISSOLVE_STEPS)))
    target = os.path.join(validation, "stage3-motion-review.gif")
    os.makedirs(validation, exist_ok=True)
    sequence[0].save(target, save_all=True, append_images=sequence[1:],
                     duration=FRAME_MS, loop=0, optimize=True)
    report["motion_review"] = dict(
        path=target, frames=len(sequence), frame_ms=FRAME_MS,
        dissolve_steps=DISSOLVE_STEPS, hold_ms_per_keyframe=FRAME_MS * DISSOLVE_STEPS,
        size=list(frames[0].size), bytes=os.path.getsize(target),
        note="design review only; not a web asset - no frontend reads this file")


def main(argv):
    args = parse_args(argv)
    root = os.path.abspath(args.renders)
    validation = os.path.abspath(args.validation)
    report = {"contact_sheets": {}, "diagnostic": {}, "motion_review": {}}
    build_contact_sheets(root, report)
    build_diagnostic(root, report)
    build_motion_review(root, validation, report)
    if args.report:
        os.makedirs(os.path.dirname(os.path.abspath(args.report)), exist_ok=True)
        with open(args.report, "w", encoding="utf-8") as handle:
            json.dump(report, handle, indent=2, sort_keys=True, default=str)
    for group in ("contact_sheets", "diagnostic"):
        for name, entry in sorted(report[group].items()):
            print("%-12s %-26s %s" % (group, name, json.dumps(
                {key: value for key, value in entry.items()
                 if key in ("path", "size", "iou", "mean_absolute_alpha_delta",
                            "skipped")}) if isinstance(entry, dict) else entry))
    print("%-12s %-26s %s" % ("motion_review", "-", json.dumps(
        {key: value for key, value in report["motion_review"].items()
         if key in ("path", "frames", "hold_ms_per_keyframe", "size", "skipped")})))
    return report


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
