"""ADA screening criteria shared by the eval harness and report.

Honesty rule (load-bearing, do not relax): the model assesses presence/absence
of features visible in a photo. Slope percentages and widths in inches are not
measurable from imagery — door_width_adequate is capped at an appearance-level
vocabulary and is excluded from strict accuracy scoring.
"""

# Decision rules below were earned by the 2026-09-03 error adjudication: every
# clause targets a confirmed failure mode, so trim with care.
CRITERIA = [
    ("step_free_entry",
     "Entrance is level with the sidewalk - no steps or raised threshold. CAUTION: "
     "a raised platform poured in the same concrete tone as the sidewalk looks flat "
     "from head-on, especially when shot standing on the platform itself. Answer "
     "present only if a view actually shows the ground plane running level from "
     "sidewalk to threshold; look in oblique views for a shadowed riser edge."),
    ("ramp_present",
     "A ramp (permanent or portable) serving the entrance. Ramps are often OFF-AXIS: "
     "at the side of the entrance, brick or stone surfaced, with railings that look "
     "like ordinary fencing. Check the edges of any platform in every view before "
     "answering absent; a sloped surface meeting the entrance level counts."),
    ("handrails_present",
     "Handrails on any visible steps or ramp serving the entrance (if the entrance "
     "has no steps and no ramp, answer absent)"),
    ("auto_door_button",
     "An automatic door opener push-button is visible"),
    ("lever_or_pull_hardware",
     "Graspable door hardware operable with a closed fist: a lever handle, "
     "horizontal push-bar, or loop/D pull that stands off the door surface enough "
     "to wrap fingers behind. A flat PUSH PLATE is NOT pull hardware even when tall "
     "and brass; a round knob is NOT; a surface-mounted latch bracket is NOT a "
     "lever. Knob plus push plate = absent."),
    ("clear_approach",
     "The direct WALKING LINE from sidewalk to door is unobstructed. Count only "
     "objects actually standing IN that line. Furniture, signs, or umbrellas to the "
     "side or overhead - even when they visually overlap the doorway from an oblique "
     "angle - do NOT count. A railing PARALLEL to the path (edge protection) does "
     "not count; only a barrier ACROSS the path does."),
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
