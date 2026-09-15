"""Hero v2 — Stage 3 closure: pivot-offset sweep, scoring, and winner selection.

    python Design-Assets/hero-v2/scripts/optimize_stage3_pivot.py \
      --root   Design-Assets/hero-v2 \
      --out    Design-Assets/hero-v2/validation/stage3-optimizer \
      --phase  sweep

Runs the real Stage 3 builder (no renders: `--skip-renders`) once per pivot candidate,
because the only honest way to know whether a pivot offset fixes the FRAME_04 crowding is to
let the actual scene, cameras, sequence fit and relation curves recompute. Each candidate
then has to clear the hard constraints before it is ranked at all:

* minimum form gap >= 5 px on every frame and device (scaled to the real page slot)
* no clipping: the margin contract holds on every state
* no node inside the desktop text-safe region or the mobile margin strips
* core drift <= 2.5% of the frame width
* apparent scale delta <= 12% per step, core scale delta <= 1%
* every consecutive step smaller than the direct frame 01 -> frame 04 change
* frame 04 meaningfully different from frame 01

Ranking follows the card's priority: strongest 01->04 difference, then smooth continuity,
then the largest minimum gap, then the smallest core drift - as weights, so a candidate
cannot win on movement alone while making the sequence stutter.
"""

from __future__ import annotations

import argparse
import glob
import json
import math
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_BLENDER = "/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
WEIGHTS = dict(movement=0.35, continuity=0.30, gap=0.20, drift=0.15)
STEPS = ((1, 2), (2, 3), (3, 4))
FAR = (1, 4)
# The checker carries its own copy of the contract, read from the card rather than imported
# from the library: `hero_v2_stage3` imports bpy and only exists inside Blender, and a
# checker that shares the implementation's constants cannot catch the implementation.
CONTRACT = dict(
    min_gap_px=5.0, preferred_gap_px=8.0, safety_gap_px=6.0, core_drift_max_pct=2.5,
    scale_max_pct=12.0, core_scale_max_pct=1.0,
    desktop_clearance_pct=7.9, mobile_clearance_pct=3.9,
    desktop_safe_text_region=(0.015, 0.050, 0.085, 0.950),
    mobile_safe_regions=((0.0, 0.0, 1.0, 0.045), (0.0, 0.955, 1.0, 1.0)),
    pivot_sweep=(0.00, 0.04, 0.06, 0.08, 0.10, 0.12, 0.14, 0.16),
)


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, help="Design-Assets/hero-v2")
    parser.add_argument("--out", required=True, help="validation/stage3-optimizer")
    parser.add_argument("--blender", default=os.environ.get("BLENDER", DEFAULT_BLENDER))
    parser.add_argument("--phase", default="sweep",
                        choices=("sweep", "rescore", "sheets"))
    parser.add_argument("--scales", default=None,
                        help="comma-separated override of the magnitude sweep")
    parser.add_argument("--signs", default="1,-1")
    parser.add_argument("--winner", default=None, help="candidate id for --phase sheets")
    return parser.parse_args(argv)


def run_builder(args, scale, sign, workdir):
    os.makedirs(workdir, exist_ok=True)
    report_path = os.path.join(workdir, "candidate-report.json")
    blend_path = os.path.join(workdir, "candidate.blend")
    command = [args.blender, "--background", "--factory-startup", "--python",
               os.path.join(HERE, "build_hero_v2_stage3.py"), "--",
               "--blend-out", blend_path, "--renders",
               os.path.join(workdir, "renders", "stage3"), "--report", report_path,
               "--skip-renders", "--pivot-scale", str(scale), "--pivot-sign", str(sign)]
    completed = subprocess.run(command, capture_output=True, text=True)
    if completed.returncode != 0 or not os.path.exists(report_path):
        tail = (completed.stdout or "")[-1200:] + (completed.stderr or "")[-1200:]
        return None, dict(scale=scale, sign=sign, error="builder failed",
                          tail=tail.splitlines()[-6:])
    with open(report_path, "r", encoding="utf-8") as handle:
        return json.load(handle), dict(scale=scale, sign=sign)


def safe_region_intrusion(report):
    """Analytic check of the declared text-safe regions, from the recorded projections.

    A node's projected disc is approximated by its centroid plus its apparent radius; that
    is conservative (a disc can only reach as far as its radius) and needs no render.
    """
    worst, detail = 0, {}
    for state_key, devices in report.get("projections", {}).items():
        for device, nodes in devices.items():
            regions = [CONTRACT["desktop_safe_text_region"]] if device == "desktop" else \
                list(CONTRACT["mobile_safe_regions"])
            for group, entry in nodes.items():
                cx, cy = entry["centroid"]
                radius = entry["apparent_diameter_pct"] / 200.0
                for region in regions:
                    x0, y0, x1, y1 = region
                    overlap_x = min(cx + radius, x1) - max(cx - radius, x0)
                    overlap_y = min(cy + radius, y1) - max(cy - radius, y0)
                    if overlap_x > 0 and overlap_y > 0:
                        fraction = overlap_x * overlap_y
                        worst = max(worst, fraction)
                        detail["%s/%s/%s" % (state_key, device, group)] = round(
                            fraction, 6)
    return worst, detail


def evaluate(report):
    """Turn one candidate report into the card's measurement set plus the hard verdict."""
    state_keys = [entry["key"] for entry in report.get("state_transforms", [])]
    measured = dict(
        min_gap_px={}, edge_clearance_pct={}, core_shift_pct={},
        companion_shift_pct={}, scale_delta_pct={}, anchors_ok=True, notes=[])
    for state_key, entry in report.get("composition", {}).items():
        for device in ("desktop", "mobile"):
            measured["min_gap_px"].setdefault(state_key, {})[device] = \
                entry[device]["min_gap_scaled_to_page_px"]
            measured["edge_clearance_pct"].setdefault(state_key, {})[device] = round(
                min(entry[device]["edge_clearance_pct"].values()), 3)
    projections = report.get("projections", {})
    for first, second in STEPS + (FAR,):
        a = projections[state_keys[first - 1]]
        b = projections[state_keys[second - 1]]
        for device in ("desktop", "mobile"):
            before, after = a[device], b[device]
            pair = "%d->%d" % (first, second)
            measured["core_shift_pct"].setdefault(pair, {})[device] = round(
                100.0 * math.hypot(
                    after["GRP_CORE"]["centroid"][0] - before["GRP_CORE"]["centroid"][0],
                    after["GRP_CORE"]["centroid"][1] - before["GRP_CORE"]["centroid"][1]),
                3)
            measured["companion_shift_pct"].setdefault(pair, {})[device] = {
                group: round(100.0 * math.hypot(
                    after[group]["centroid"][0] - before[group]["centroid"][0],
                    after[group]["centroid"][1] - before[group]["centroid"][1]), 3)
                for group in ("GRP_HUMAN_CENTERED_AI", "GRP_HEALTH_BEHAVIOR",
                              "GRP_WEARABLE_EDGE")}
            measured["scale_delta_pct"].setdefault(pair, {})[device] = {
                group: round(100.0 * (after[group]["apparent_diameter_pct"] /
                                      before[group]["apparent_diameter_pct"] - 1.0), 2)
                for group in ("GRP_CORE", "GRP_HUMAN_CENTERED_AI",
                              "GRP_HEALTH_BEHAVIOR", "GRP_WEARABLE_EDGE")}
    for state_key, state_anchors in report.get("anchors", {}).items():
        for group, entry in state_anchors.items():
            if not (entry.get("start_ok") and entry.get("end_ok")):
                measured["anchors_ok"] = False
                measured["notes"].append("anchor failed: %s/%s" % (state_key, group))
    intrusion, intrusion_detail = safe_region_intrusion(report)
    measured["safe_region_overlap"] = round(intrusion, 6)
    measured["safe_region_detail"] = intrusion_detail

    min_gap = min(value for entry in measured["min_gap_px"].values()
                  for value in entry.values())
    clearance_by_device = {
        device: min(entry[device] for entry in measured["edge_clearance_pct"].values())
        for device in ("desktop", "mobile")}
    core_drift = max(value for entry in measured["core_shift_pct"].values()
                     for value in entry.values())
    far_groups = measured["companion_shift_pct"]["1->4"]["desktop"]
    movement = sum(far_groups.values()) / max(len(far_groups), 1)
    step_ratios = []
    far_desktop = measured["companion_shift_pct"]["1->4"]["desktop"]
    for pair in ("1->2", "2->3", "3->4"):
        step = measured["companion_shift_pct"][pair]["desktop"]
        step_ratios.append(max(step[group] / max(far_desktop[group], 1e-6)
                               for group in step))
    continuity_ratio = max(step_ratios)
    scale_ok = all(abs(value) <= 12.0
                   for pair, entry in measured["scale_delta_pct"].items()
                   if pair != "1->4" for group, value in entry["desktop"].items()
                   if group != "GRP_CORE") and \
        all(abs(value) <= 1.0 for pair, entry in measured["scale_delta_pct"].items()
            for group, value in entry["desktop"].items() if group == "GRP_CORE")
    far_iou_proxy = 1.0 - movement / 100.0
    constraints = {
        "gap_every_frame_device": dict(
            pass_=min_gap >= CONTRACT["min_gap_px"], value=min_gap,
            required=CONTRACT["min_gap_px"]),
        "no_clipping": dict(
            pass_=clearance_by_device["desktop"] >= CONTRACT["desktop_clearance_pct"] and
            clearance_by_device["mobile"] >= CONTRACT["mobile_clearance_pct"],
            desktop=clearance_by_device["desktop"],
            mobile=clearance_by_device["mobile"],
            required=dict(desktop=CONTRACT["desktop_clearance_pct"],
                          mobile=CONTRACT["mobile_clearance_pct"]),
            note="each device has its own margin contract (8% desktop, 4% mobile), so a "
                 "single combined threshold would fail the mobile frame for being mobile"),
        "safe_region_clear": dict(pass_=intrusion == 0.0, value=intrusion),
        "core_drift_small": dict(pass_=core_drift <= CONTRACT["core_drift_max_pct"],
                                 value=core_drift,
                                 limit=CONTRACT["core_drift_max_pct"]),
        "scale_delta_bounded": dict(pass_=scale_ok, ratio=continuity_ratio),
        "continuity_steps_smaller_than_total": dict(pass_=continuity_ratio < 1.0,
                                                    ratio=continuity_ratio),
        "frame_04_differs_from_01": dict(pass_=far_iou_proxy <= 0.97, value=far_iou_proxy),
        "endpoints_anchored": dict(pass_=measured["anchors_ok"]),
    }
    hard_pass = all(entry["pass_"] for entry in constraints.values())
    return dict(measured=measured, constraints=constraints, hard_pass=hard_pass,
                min_gap_px=min_gap, min_clearance_pct=clearance_by_device,
                core_drift_pct=core_drift, movement_pct=round(movement, 3),
                continuity_ratio=round(continuity_ratio, 4),
                authored=report.get("state_transforms", []),
                pivot=report.get("pivot", {}))


def score(candidates):
    passing = [entry for entry in candidates if entry["hard_pass"]]
    if not passing:
        return None
    gaps = [entry["min_gap_px"] for entry in passing]
    movements = [entry["movement_pct"] for entry in passing]
    drifts = [entry["core_drift_pct"] for entry in passing]

    def normalise(value, values, invert=False):
        low, high = min(values), max(values)
        if high - low < 1e-9:
            return 1.0
        ratio = (value - low) / (high - low)
        return 1.0 - ratio if invert else ratio

    for entry in passing:
        entry["score"] = round(
            WEIGHTS["movement"] * normalise(entry["movement_pct"], movements) +
            WEIGHTS["continuity"] * normalise(entry["continuity_ratio"],
                                              [e["continuity_ratio"] for e in passing],
                                              invert=True) +
            WEIGHTS["gap"] * normalise(entry["min_gap_px"], gaps) +
            WEIGHTS["drift"] * normalise(entry["core_drift_pct"], drifts, invert=True), 5)
        entry["preferred_gap"] = entry["min_gap_px"] >= CONTRACT["preferred_gap_px"]
        # The 8 px preference is not reachable on this rig without an offset so large that
        # the companions start reading as translated rather than rotated. A candidate that
        # only just clears the 5 px floor is also a bad winner: the final validator measures
        # the gap from rendered pixels, not from projections, so a 6% margin over the floor
        # is a coin flip. Hence the safety rank: a healthy gap first, then the card's
        # priority order.
        entry["safety_gap"] = entry["min_gap_px"] >= CONTRACT["safety_gap_px"]
    passing.sort(key=lambda entry: (entry["preferred_gap"], entry["safety_gap"],
                                    entry["score"]), reverse=True)
    return passing[0]


def run_quiet(command, log_path):
    os.makedirs(os.path.dirname(os.path.abspath(log_path)), exist_ok=True)
    with open(log_path, "w", encoding="utf-8") as handle:
        completed = subprocess.run(command, stdout=handle, stderr=subprocess.STDOUT,
                                   text=True)
    return completed.returncode


def write_summary(out, candidates, winner, scales, signs):
    summary = dict(
        contract=CONTRACT, weights=WEIGHTS,
        sweep=dict(scales=scales, signs=signs,
                   authored=(candidates[0].get("authored") if candidates else [])),
        candidates=[{key: value for key, value in entry.items()
                     if key in ("id", "scale", "sign", "hard_pass", "min_gap_px",
                                "min_clearance_pct", "core_drift_pct", "movement_pct",
                                "continuity_ratio", "score", "preferred_gap",
                                "safety_gap", "pivot", "constraints", "error")}
                    for entry in candidates],
        winner=winner["id"] if winner else None,
        winner_detail=winner)
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "stage3-optimizer-summary.json"), "w",
              encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True, default=str)
    lines = ["# Hero v2 — Stage 3 pivot-offset sweep", "",
             "Constrained closure pass: the authored angles are unchanged and the FRAME_04",
             "crowding is solved by moving the rotation pivot along the direction derived",
             "from the core -> HEALTH vector. Every row is a real scene build with the",
             "sequence fit, cameras and relation curves recomputed.", "",
             "| candidate | offset | min gap px | clearance d/m % | 01->04 movement % | "
             "continuity | core drift % | hard | score |",
             "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for entry in candidates:
        if entry.get("error"):
            lines.append("| %s | %.2f | — | — | — | — | — | FAIL (builder) | — |"
                         % (entry["id"], entry["scale"]))
            continue
        clearance = entry["min_clearance_pct"]
        lines.append("| %s | %.2f | %.2f | %.2f / %.2f | %.2f | %.3f | %.2f | %s | %s |"
                     % (entry["id"], entry["scale"], entry["min_gap_px"],
                        clearance["desktop"], clearance["mobile"], entry["movement_pct"],
                        entry["continuity_ratio"], entry["core_drift_pct"],
                        "PASS" if entry["hard_pass"] else "FAIL", entry.get("score", "—")))
    lines += ["", "Winner: **%s**" % (winner["id"] if winner else "none"),
              "", "Ranking: hard constraints first, then the %.0f px preference, then a"
              % CONTRACT["preferred_gap_px"],
              "%.0f px safety gap (the final validator measures rendered pixels, not"
              % CONTRACT["safety_gap_px"],
              "projections), then weights movement %.2f / continuity %.2f / gap %.2f /"
              % (WEIGHTS["movement"], WEIGHTS["continuity"], WEIGHTS["gap"]),
              "drift %.2f." % WEIGHTS["drift"]]
    with open(os.path.join(out, "stage3-optimizer-summary.md"), "w",
              encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")
    return summary


def main(argv):
    args = parse_args(argv)
    out = os.path.abspath(args.out)
    workdir = os.path.join(out, "sweep-work")
    os.makedirs(workdir, exist_ok=True)
    scales = [float(value) for value in args.scales.split(",")] if args.scales else \
        list(CONTRACT["pivot_sweep"])
    signs = [int(value) for value in args.signs.split(",")]
    candidates = []
    if args.phase == "rescore":
        # Re-score the reports already on disk: the sweep is expensive, the criteria are not.
        order = {value: index for index, value in enumerate(sorted(scales))}
        for path in sorted(glob.glob(os.path.join(workdir, "*",
                                                  "candidate-report.json"))):
            identifier = os.path.basename(os.path.dirname(path))
            with open(path, "r", encoding="utf-8") as handle:
                report = json.load(handle)
            evaluated = evaluate(report)
            pivot = report.get("pivot", {})
            evaluated.update(dict(id=identifier, scale=pivot.get("scale", 0.0),
                                  sign=pivot.get("sign", 1)))
            candidates.append(evaluated)
        candidates.sort(key=lambda entry: order.get(entry.get("scale"), 99))
        winner = score(candidates)
        summary = write_summary(out, candidates, winner, sorted(scales), signs)
        for entry in candidates:
            print("  %-14s gap %6.2f hard %-5s safety %-5s score %s"
                  % (entry["id"], entry["min_gap_px"], entry["hard_pass"],
                     entry.get("safety_gap"), entry.get("score")))
        print("RESCORE winner: %s" % summary["winner"])
        return summary
    if args.phase == "sheets":
        # Quick contact sheets for the leading candidates. candidate-01 is the winner; the
        # others exist so the choice can be seen, not just read.
        chosen = [float(value) for value in args.scales.split(",")]
        for index, scale in enumerate(chosen, start=1):
            tag = "candidate-%02d" % index
            target = os.path.join(out, tag)
            renders = os.path.join(target, "renders", "stage3")
            os.makedirs(renders, exist_ok=True)
            label = "%s (pivot %.2f%s)" % (tag, scale,
                                           ", WINNER" if index == 1 else "")
            print("building %s" % label, flush=True)
            run_quiet([args.blender, "--background", "--factory-startup", "--python",
                       os.path.join(HERE, "build_hero_v2_stage3.py"), "--",
                       "--blend-out", os.path.join(target, "stage3-quick.blend"),
                       "--renders", renders,
                       "--report", os.path.join(target, "stage3-report-quick.json"),
                       "--quick", "--pivot-scale", str(scale), "--pivot-sign", "1"],
                      os.path.join(target, "build-quick.log"))
            run_quiet([sys.executable, os.path.join(HERE, "composite_stage3.py"),
                       "--renders", renders,
                       "--report", os.path.join(target, "composite-quick.json")],
                      os.path.join(target, "composite-quick.log"))
            run_quiet([sys.executable, os.path.join(HERE, "contact_sheet_stage3.py"),
                       "--renders", renders, "--validation",
                       os.path.join(target, "validation"),
                       "--report", os.path.join(target, "sheets-quick.json")],
                      os.path.join(target, "sheets-quick.log"))
            promoted = []
            for name in ("contact-desktop-dark.png", "contact-desktop-light.png",
                         "contact-mobile-dark.png", "contact-mobile-light.png",
                         "contact-motion-difference-desktop-dark.png",
                         "contact-motion-difference-mobile-dark.png"):
                source = os.path.join(renders, name)
                if os.path.exists(source):
                    shutil.copy2(source, os.path.join(target, name))
                    promoted.append(name)
            print("  %s -> %d sheets" % (label, len(promoted)), flush=True)
        return None
    for scale in scales:
        for sign in signs:
            identifier = "k%.2f-s%s" % (scale, "plus" if sign > 0 else "minus")
            report, meta = run_builder(args, scale, sign,
                                       os.path.join(workdir, identifier))
            if report is None:
                candidates.append(dict(id=identifier, scale=scale, sign=sign,
                                       hard_pass=False, error=meta))
                print("%-14s builder failed %s" % (identifier, meta.get("tail")))
                continue
            evaluated = evaluate(report)
            evaluated.update(dict(id=identifier, scale=scale, sign=sign))
            candidates.append(evaluated)
            failed = [name for name, entry in evaluated["constraints"].items()
                      if not entry["pass_"]]
            print("%-14s gap %6.2f clr d%5.2f/m%5.2f move %6.2f cont %.3f drift %4.2f %s"
                  % (identifier, evaluated["min_gap_px"],
                     evaluated["min_clearance_pct"]["desktop"],
                     evaluated["min_clearance_pct"]["mobile"],
                     evaluated["movement_pct"], evaluated["continuity_ratio"],
                     evaluated["core_drift_pct"],
                     "PASS" if evaluated["hard_pass"] else "FAIL %s" % failed),
                  flush=True)
    winner = score(candidates)
    summary = write_summary(out, candidates, winner, scales, signs)
    print("\nWINNER: %s" % (winner["id"] if winner else "NONE (no candidate passed)"))
    return summary


if __name__ == "__main__":
    main(sys.argv[1:])
