# EntryMap build-ready handoff design

Date: 2026-09-05

## Objective

Extend the verified EntryMap production package into a build-ready design handoff without redrawing, recoloring, retyping, or otherwise altering the approved brand artwork or the seven approved root mockup/logo boards.

The expanded package must let a product designer and application engineer answer four questions without guessing:

1. Which screen or state is being built?
2. What can the person do from that state, and where does each action lead?
3. Which reusable component, asset, token, and data field renders each part of the screen?
4. What changes for guests, signed-in public contributors, business owners, accessibility profiles, permissions, offline use, stale evidence, and reduced motion?

## Approaches considered

### A. Crop-only extraction

Export each visible phone frame from the approved boards and leave the existing interaction specification as the handoff. This is maximally faithful but does not provide reusable map layers, route definitions, state ownership, or data contracts.

### B. Fully redraw every screen

Recreate the boards as new editable vectors and derive the individual screens from those files. This offers editability but creates an unacceptable risk of changing the approved logo, palette, typography, spacing, and illustrated map treatment.

### C. Hybrid handoff — selected

Preserve the approved boards byte-for-byte, create pixel-faithful individual screen and overlay exports from them, build independent vector demo-map layers using the canonical design tokens, and add implementation documents that map screens to routes, components, states, events, and data. This provides fidelity and implementation clarity without pretending that raster mockups are editable application source.

## Deliverables

### 1. Approved-source preservation

- Keep all seven approved root PNG files byte-identical.
- Keep the approved full logo and compact header lockup byte-identical in `asset-library/canonical-brand`.
- Retain the canonical SHA-256 manifest.
- Do not generate unofficial logo, wordmark, app-icon, monochrome, transparent, or vector variants.

### 2. Individual screen exports

Create `screen-exports/` containing separate PNG files for every discrete phone screen, bottom sheet, dialog, receipt inset, and meaningful app state shown on the six approved flow boards.

Each export receives:

- a stable screen ID;
- a human-readable filename;
- its source board and crop coordinates in `screen-export-manifest.json`;
- pixel dimensions and SHA-256 hash;
- a label identifying it as a screen, overlay, sheet, dialog, receipt, or state.

The crops must preserve the approved pixels. They must not be regenerated or visually cleaned up.

### 3. Reusable demo-map kit

Create `map-kit/` with independent SVG and PNG layers for the presentation/demo map:

- map base with pale-lavender land and high-contrast streets;
- blocks/building footprints;
- street labels;
- park/water accents when present;
- pin placement sample;
- empty-area version;
- before-profile and after-profile versions;
- selected-business version;
- owner-confirmed, scanned, and estimated examples;
- mixed-cluster example;
- map safe-area and pin-anchor guidance.

The map kit is illustrative demo artwork, not geographic truth, navigation data, or a replacement for a map provider. The handoff must say this plainly and include guidance for mapping the visual style onto Mapbox, MapLibre, Google Maps, or another production provider.

### 4. Screen inventory and route map

Create `handoff/SCREEN-INVENTORY.md` and `handoff/ROUTE-MAP.md`.

The route map covers:

- first launch and skippable needs profile;
- guest map exploration and temporary filters;
- account creation/sign-in only when saving or contributing requires it;
- map, scan, and profile peer navigation;
- business sheet and evidence receipt hierarchy;
- live scan and offline saved scan;
- suggestion/correction flow;
- owner claim entry from a business profile;
- owner evidence submission and owner workspace;
- camera permission, empty area, processing, published, offline, stale evidence, and re-check paths.

Public and disabled-user experiences remain one universal public product shaped by optional needs filters. Trust tier is never a filter. Owner tools are a separate authenticated workspace reached through claiming a business, not a separate consumer application.

### 5. Flow-to-screen mapping

Create `handoff/FLOW-MAP.md` and `handoff/FLOW-MATRIX.csv`.

Every flow row identifies:

- flow and step ID;
- role and authentication state;
- starting screen;
- user action;
- validation or permission condition;
- destination screen or state;
- transition and timing token;
- analytics event name;
- recovery/back behavior;
- reduced-motion result.

### 6. Screen/state matrix

Create `handoff/SCREEN-STATE-MATRIX.csv` covering loading, populated, empty, offline, permission-limited, needs-attention, aging evidence, and reduced-motion variations where applicable. Negative trust grades, red error styling, gray disabled styling, owner “verified” language, shields, and an auditor tier remain prohibited.

### 7. Component mapping

Create `handoff/COMPONENT-MAP.md` and `handoff/COMPONENT-MATRIX.csv` mapping each visible element to:

- component name;
- asset IDs from `asset-manifest.json`;
- design tokens;
- variants and interaction states;
- required accessible name and semantics;
- owning screen IDs;
- implementation notes.

### 8. Data contracts

Create `handoff/DATA-MODEL.md` and machine-readable `handoff/data-contracts.json` for:

- business;
- entrance;
- accessibility profile;
- entrance feature claim;
- evidence source;
- evidence receipt;
- provenance line;
- confidence;
- freshness;
- trust tier;
- match result;
- correction suggestion;
- scan session;
- owner claim;
- public/state record.

Trust is computed and rendered separately from needs matching, freshness, confidence, provenance, and selection. Pins only upgrade through the fixed three-tier ladder.

### 9. Responsive and implementation guidance

Create:

- `handoff/RESPONSIVE-SPEC.md` for compact, standard, large-phone, tablet, and projector/demo behavior;
- `handoff/ACCESSIBILITY-CHECKLIST.md` covering WCAG AA, target 7:1 body contrast, 48 px targets, focus, screen-reader announcements, color-independent encodings, and reduced motion;
- `handoff/MAP-IMPLEMENTATION.md` covering map camera behavior, clustering, z-order, anchors, state layering, and provider-neutral styling;
- `handoff/ENGINEERING-HANDOFF.md` with recommended module boundaries and acceptance checks.

### 10. Package index and verification

Create `START-HERE.md` as the package entry point and `PACKAGE-MANIFEST.json` containing every file path, byte size, SHA-256 hash, and category.

The final verification must confirm:

- approved sources and existing mockup boards remain byte-identical;
- every screen export matches its documented source crop;
- every SVG parses as XML;
- every PNG has the expected dimensions and visible pixels;
- flow, screen, component, and data references resolve;
- no prohibited old palette values or reconstructed wordmark code remain;
- the ZIP contains every source file exactly once and all archive hashes match.

## Visual and interaction rules that remain fixed

- Canonical palette: deep indigo `#1E1142`, violet `#4F34DB`, sky blue `#76BCFD`, marigold `#FDB327`, lavender path `#CFBCEE`, UI lavender `#F5F2FC` and `#E8E1F7`, white `#FFFFFF`.
- Estimated: hollow, dashed sky pin, italic information symbol, no check.
- Scanned on-site: solid marigold pin, person symbol, two of three evidence segments.
- Owner-confirmed: solid violet pin, storefront symbol, three of three evidence segments, separate outlined check.
- Texas state information is provenance, not a trust tier and not a map-pin decoration.
- Needs matching uses an external solid/dashed/dotted halo and never recolors the trust pin.
- Evidence strength affects tier size within each map context; selection, freshness, and clustering use independent visual layers.
- The theatrical live scan remains under eight seconds and has an instant reduced-motion end state.

## Completion definition

The expanded package is complete when a designer can find any approved screen as its own image, an engineer can trace every documented action to a destination and data contract, and neither needs to infer brand colors, pin meaning, hierarchy, map layering, role boundaries, or accessibility behavior from a composite presentation board.
