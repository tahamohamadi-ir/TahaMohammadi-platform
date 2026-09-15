"""Stage 4.2 — relation-curve legibility micro-pass (candidates and overrides only).

This module never re-authors a locked value. It *drives* the approved Stage 3 builder
(`build_hero_v2_stage3.main`) with one documented delta: the relation stroke's apparent weight and
its per-theme contrast gain. Geometry, animation, cameras, materials of the spheres, sampling,
denoise and alpha handling all stay the Stage 3 code paths.

Measured baseline (Stage 4.1, delivered size): desktop light ~1.3:1 and mobile light ~1.5-1.8:1
against their page backgrounds — BORDERLINE against the 3:1 non-text bar. Stage 3's stroke is
`#C6B191` at `CURVE_TUBE_RADIUS = 0.0037` with theme gains dark 1.00 / light 0.22.

Candidate bands from the card (not blind fixed values; tuned inside the bands only if the
measurements justify it):

    A  baseline          1.00x radius,  dark 1.00 / light 0.22   (Stage 3 / Stage 2.7 as approved)
    B  medium           +25% radius,    dark 1.15 / light 0.16
    C  strong           +40% radius,    dark 1.30 / light 0.12

Theme-specific treatment is deliberate: dark moves toward champagne so it separates from navy,
light moves toward a darker warm stone so it stops disappearing into #f7f8f5. No glow, no emission,
no new objects.
"""

CANDIDATES = {
    'A': {
        'label': 'baseline',
        'radius_scale': 1.00,
        'dark_gain': 1.00,
        'light_gain': 0.22,
        'note': 'Stage 3 / Stage 2.7 relation treatment, unchanged',
    },
    'B': {
        'label': 'medium legibility',
        'radius_scale': 1.25,
        'dark_gain': 1.15,
        'light_gain': 0.16,
        'note': '+25% apparent weight, modest contrast increase, still subordinate',
    },
    'C': {
        'label': 'strong legibility',
        'radius_scale': 1.40,
        'dark_gain': 1.30,
        'light_gain': 0.12,
        'note': '+40% apparent weight, stronger contrast, risk of reading technical',
    },
}

# D is the calibrated hybrid the measured reviews asked for: the same physical weight as candidate
# B's band top, with the two themes calibrated independently because their reviews disagreed.
#   dark  - both A and B failed "noticed without searching" (only C passed, at the cost of reading
#           technical), so the dark-side contrast sits between B and C.
#   light - B was the clear winner (A broke into detached fragments, C turned diagrammatic),
#           so the light-side gain stays exactly B's.
# The physical radius is shared (one relation, one geometry); only the per-theme material preset
# differs, which the card allows explicitly.
CANDIDATES['D'] = {
    'label': 'calibrated hybrid (B band top, dark calibrated up, light as B)',
    'radius_scale': 1.30,
    'dark_gain': 1.24,
    'light_gain': 0.16,
    'note': 'in-band fine-tune justified by the delivered-scale reviews',
}

ORDER = ('A', 'B', 'C', 'D')

# The Stage 3 render set is the full matrix; the candidate decision uses FRAME_03, which the card
# prefers as the high-information state. Nothing is rendered twice.
DECISION_STATE = '03'


def apply_overrides(candidate):
    """Patch the imported Stage 2.7 curve constants for one candidate.

    `build_relation_curve` binds `tube_radius=CURVE_TUBE_RADIUS` at *definition* time, so patching
    the module attribute alone would silently do nothing — the default is rebound explicitly and the
    change is reported by the caller. The theme gains are read from `THEME_PRESET` at call time.
    """
    import hero_v2_stage2_7 as s27

    spec = CANDIDATES[candidate]
    # The base radius is captured once: calling this twice in one process must not compound the
    # scale (the module attribute is overwritten, not multiplied, from the recorded baseline).
    if not hasattr(s27, 'CURVE_TUBE_RADIUS_BASE'):
        s27.CURVE_TUBE_RADIUS_BASE = s27.CURVE_TUBE_RADIUS
    s27.CURVE_TUBE_RADIUS = s27.CURVE_TUBE_RADIUS_BASE * spec['radius_scale']

    # Rebind the bound default so the builder really uses the scaled radius.
    defaults = list(s27.build_relation_curve.__defaults__ or ())
    if not defaults:
        raise RuntimeError('build_relation_curve has no bound default to rebind')
    defaults[-1] = s27.CURVE_TUBE_RADIUS
    s27.build_relation_curve.__defaults__ = tuple(defaults)

    s27.THEME_PRESET['dark']['stroke'] = spec['dark_gain']
    s27.THEME_PRESET['light']['stroke'] = spec['light_gain']

    return {
        'candidate': candidate,
        'label': spec['label'],
        'curve_tube_radius': round(s27.CURVE_TUBE_RADIUS, 6),
        'bound_default': round(s27.build_relation_curve.__defaults__[-1], 6),
        'dark_stroke_gain': s27.THEME_PRESET['dark']['stroke'],
        'light_stroke_gain': s27.THEME_PRESET['light']['stroke'],
    }
