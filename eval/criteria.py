"""ADA screening criteria shared by the eval harness and report.

Honesty rule (load-bearing, do not relax): the model assesses presence/absence
of features visible in a photo. Slope percentages and widths in inches are not
measurable from imagery — door_width_adequate is capped at an appearance-level
vocabulary and is excluded from strict accuracy scoring.
"""

CRITERIA = [
    ("step_free_entry",
     "Entrance is level with the sidewalk - no steps or raised threshold visible"),
    ("ramp_present",
     "A ramp (permanent or portable) serving the entrance is visible"),
    ("handrails_present",
     "Handrails on any visible steps or ramp"),
    ("auto_door_button",
     "An automatic door opener push-button is visible"),
    ("lever_or_pull_hardware",
     "Door hardware is lever-style, push-bar, or loop pull (not a round knob)"),
    ("clear_approach",
     "The path to the door is free of obstructions (signs, merchandise, bikes)"),
    ("accessible_signage",
     "International Symbol of Accessibility or directional accessibility signage visible"),
    ("door_width_adequate",
     "REQUIRES MEASUREMENT - clear width >= 32 inches cannot be measured from a "
     "photo; assess only as appears_wide / appears_narrow / cannot_tell"),
]

CRITERIA_KEYS = [key for key, _ in CRITERIA]

# Verdict vocabularies per criterion
STANDARD_VERDICTS = {"present", "absent", "not_visible"}
WIDTH_VERDICTS = {"appears_wide", "appears_narrow", "cannot_tell"}


def allowed_verdicts(key: str) -> set:
    return WIDTH_VERDICTS if key == "door_width_adequate" else STANDARD_VERDICTS
