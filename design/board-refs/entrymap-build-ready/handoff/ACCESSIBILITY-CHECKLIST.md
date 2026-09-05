# Accessibility acceptance checklist

## Perceptual

- [ ] Body text meets at least WCAG AA and targets 7:1 against its surface.
- [ ] Large display text and icons meet at least 3:1; focus indicators meet 3:1 against adjacent colors.
- [ ] Estimated, Scanned on-site, and Owner-confirmed remain distinguishable by shape, icon, color, ring completion, and text.
- [ ] Good, partial, and unknown matches remain distinguishable by solid, dashed, and dotted outlines plus a text label where details are shown.
- [ ] No information depends on red, gray, hue, glow, animation, or pin size alone.
- [ ] Texas/public-record provenance is named in text and never masquerades as a trust tier.
- [ ] At 200% text size, content reflows without clipping, overlap, or loss of controls.

## Operable

- [ ] Every interactive target is at least 48×48 CSS pixels with adequate separation.
- [ ] Keyboard, switch, and assistive-technology focus order follows visual reading order.
- [ ] Focus is visibly indicated with the 3 px sky ring and 3 px offset.
- [ ] Opening a sheet moves focus to its heading; closing returns focus to the opening pin/control.
- [ ] Map pins are reachable through an equivalent ordered nearby-results list.
- [ ] Drag-only sheet movement has explicit Expand, Collapse, and Close actions.
- [ ] Camera capture has an explicit button and does not depend on a gesture.

## Understandable

- [ ] Controls use consistent action names: Publish → Published; Send suggestion → Suggestion sent.
- [ ] Unknown claims read “Not yet seen — be the first to scan.”
- [ ] Aging evidence describes elapsed time and the re-check action, never a failing place.
- [ ] Owner language uses “Owner-confirmed,” never “verified,” “certified,” a shield, or legal-compliance language.
- [ ] Feature chips contain only visually confirmed observations and never “ADA compliant.”
- [ ] Permission prompts are preceded by plain-language primers and always include a useful alternative.

## Motion and announcements

- [ ] `prefers-reduced-motion: reduce` removes bounce, ripple, sweep, stagger, scale, and rotation.
- [ ] Reduced-motion transitions are instant or crossfade for no more than 80 ms.
- [ ] Scan checklist updates use a polite live region and completion is announced once.
- [ ] Decorative motion and map movement are not announced.
- [ ] Haptics are supplemental and respect operating-system settings.

## Evidence and media

- [ ] Source photos have alternative text describing the entrance, not inferred accessibility quality.
- [ ] Receipts expose source, date, method, witness/provenance lines, confidence, freshness, and Suggest a correction.
- [ ] Independent provenance lines remain separately readable.
- [ ] Faces and license plates are avoided or handled according to the product privacy policy.
