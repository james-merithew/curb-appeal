# EntryMap Build-Ready Handoff Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand the verified EntryMap visual package into a build-ready app handoff with individual screen exports, reusable demo-map assets, traceable flows, screen/component/data mappings, responsive and accessibility guidance, and an independently verified archive.

**Architecture:** Approved raster boards remain immutable sources. A PowerShell crop pipeline produces traceable screen exports, a focused JavaScript generator produces provider-neutral SVG demo-map variants and structured handoff files, and an independent PowerShell verifier checks hashes, dimensions, references, palette integrity, and archive parity.

**Tech Stack:** PowerShell 7, .NET `System.Drawing` and `System.IO.Compression`, Node.js ES modules, SVG 1.1, PNG, JSON, CSV, Markdown, headless Chromium for deterministic SVG rasterization.

**Spec:** `BUILD-READY-HANDOFF-DESIGN.md`

**Execution status:** Complete. All six tasks were implemented and passed the build-ready handoff verifier before archive creation.

## Global Constraints

- Preserve the seven approved root PNG files byte-for-byte.
- Preserve both canonical brand PNG files byte-for-byte and never reconstruct the logo or wordmark.
- Use only deep indigo `#1E1142`, violet `#4F34DB`, sky blue `#76BCFD`, marigold `#FDB327`, lavender path `#CFBCEE`, UI lavender `#F5F2FC` and `#E8E1F7`, and white `#FFFFFF` for core UI/map artwork.
- Keep the fixed trust ladder wording and encoding exactly as specified.
- Texas information is provenance only; trust tier is never a filter.
- Public and disabled-user experiences are one universal map with optional needs filters; owner tools are a separate authenticated workspace reached by claiming a business.
- Respect 48 px targets, WCAG AA, target 7:1 body contrast, color-independent encodings, and reduced motion.
- The demo-map kit is illustrative artwork, not geographic truth or a production map provider.

---

### Task 1: Integrity gate and crop manifest

**Files:**
- Create: `handoff/tools/verify-build-ready-handoff.ps1`
- Create: `screen-exports/screen-export-spec.json`
- Create: `handoff/tools/export-screen-crops.ps1`

**Interfaces:**
- Consumes: six immutable 1672×941 flow boards and the canonical brand hash manifest.
- Produces: `screen-export-spec.json` entries with `id`, `kind`, `source`, `x`, `y`, `width`, and `height`; PNGs in `screen-exports/png`; `screen-export-manifest.json` with hashes and dimensions.

- [ ] **Step 1: Write the failing integrity gate**

The verifier must fail when `screen-export-manifest.json`, `PACKAGE-MANIFEST.json`, map-kit manifests, required handoff documents, or expected route/component/data references are missing. It must also call the existing canonical-brand verifier.

- [ ] **Step 2: Run the gate and verify it fails**

Run:

```powershell
& ./handoff/tools/verify-build-ready-handoff.ps1 -PackageRoot .
```

Expected: nonzero exit with missing-deliverable messages.

- [ ] **Step 3: Implement the crop specification and exporter**

Define 25 source crops: four phone frames from each of boards 01–06 plus the evidence-receipt inset on board 02. Export with `System.Drawing.Bitmap.Clone`, record the original crop rectangle and SHA-256, and never resample or enhance pixels.

- [ ] **Step 4: Run the crop exporter**

Run:

```powershell
& ./handoff/tools/export-screen-crops.ps1 -PackageRoot .
```

Expected: 25 PNG files and a 25-entry manifest.

### Task 2: Provider-neutral demo-map kit

**Files:**
- Create: `handoff/tools/build-map-kit.mjs`
- Create: `map-kit/svg/*.svg`
- Create: `map-kit/png/*.png`
- Create: `map-kit/map-kit-manifest.json`
- Create: `map-kit/README.md`

**Interfaces:**
- Consumes: canonical design tokens and existing trust-pin/halo assets.
- Produces: eight 1170×800 SVG map variants with stable layer IDs and matching PNG previews.

- [ ] **Step 1: Extend the integrity gate with map assertions**

Require `base-map`, `before-profile`, `after-profile`, `selected-business`, `empty-area`, `mixed-cluster`, `pin-placement`, and `safe-areas` variants; require SVG XML validity, 1170×800 view boxes, expected layer IDs, and no forbidden palette values.

- [ ] **Step 2: Run the gate and verify the map assertions fail**

Expected: missing map variants.

- [ ] **Step 3: Generate the SVG maps**

Use stable groups `land`, `blocks`, `roads`, `labels`, `places`, `pins`, `halos`, `selection`, and `annotations`. Reference the existing canonical pin and halo SVG assets rather than drawing substitute trust pins.

- [ ] **Step 4: Rasterize previews**

Use headless Chromium with SwiftShader flags and isolated profiles, then verify all eight PNGs are visible 1170×800 images.

### Task 3: Screen, route, and flow mapping

**Files:**
- Create: `handoff/SCREEN-INVENTORY.md`
- Create: `handoff/ROUTE-MAP.md`
- Create: `handoff/FLOW-MAP.md`
- Create: `handoff/FLOW-MATRIX.csv`
- Create: `handoff/SCREEN-STATE-MATRIX.csv`

**Interfaces:**
- Consumes: the 25 stable screen IDs and interaction timing tokens.
- Produces: route IDs, flow-step IDs, action/event names, destinations, transitions, recovery behavior, and reduced-motion outcomes referenced by engineering documents.

- [ ] **Step 1: Add referential-integrity checks**

Require every `from_screen` and `to_screen` value in the flow matrix to resolve to the screen inventory or an explicitly named operating-system permission surface.

- [ ] **Step 2: Author the universal public flows**

Cover first launch, location and needs setup, guest map exploration, filtering, business/evidence receipt, correction, scanning, offline save, re-check, profile, sign-in-to-save, camera denial, and empty-area recovery.

- [ ] **Step 3: Author owner flows**

Cover claim start, business selection, ownership confirmation, review status, workspace overview, entrance editing, photo management, publishing, provenance receipt, and return to the public listing.

### Task 4: Component and data contracts

**Files:**
- Create: `handoff/COMPONENT-MAP.md`
- Create: `handoff/COMPONENT-MATRIX.csv`
- Create: `handoff/DATA-MODEL.md`
- Create: `handoff/data-contracts.json`

**Interfaces:**
- Consumes: `asset-library/asset-manifest.json`, fixed trust rules, screen inventory, and route IDs.
- Produces: reusable component names/variants, asset IDs, accessibility semantics, owning screens, entity schemas, enums, and UI derivation rules.

- [ ] **Step 1: Add component/data consistency checks**

Require every referenced asset ID to exist, every component screen ID to resolve, and all fixed enums to match the approved wording.

- [ ] **Step 2: Author component mappings**

Map navigation, pins, halos, filters, business sheets, feature chips, receipts, scan progress, feedback, fields, owner controls, and provenance rows.

- [ ] **Step 3: Author data contracts**

Define business, entrance, profile, feature claim, evidence source, receipt, provenance line, confidence, freshness, trust tier, match result, correction, scan session, owner claim, and public/state record schemas. Keep trust, match, freshness, confidence, provenance, selection, and clustering as independent fields.

### Task 5: Responsive, accessibility, and engineering handoff

**Files:**
- Create: `handoff/RESPONSIVE-SPEC.md`
- Create: `handoff/ACCESSIBILITY-CHECKLIST.md`
- Create: `handoff/MAP-IMPLEMENTATION.md`
- Create: `handoff/ENGINEERING-HANDOFF.md`
- Create: `START-HERE.md`

**Interfaces:**
- Consumes: all prior IDs, assets, tokens, and matrices.
- Produces: build order, module boundaries, acceptance criteria, phone/tablet/projector behavior, map-provider mapping, and a single package entry point.

- [ ] **Step 1: Document layout behavior**

Specify compact 320–374 px, standard 375–429 px, large 430–599 px, tablet 600–1023 px, and projector/demo 1024 px and wider behavior without shrinking touch targets.

- [ ] **Step 2: Document accessibility acceptance checks**

Cover contrast, line-style encodings, semantic labels, focus, touch targets, live regions, text scaling, high contrast, keyboard/switch navigation, and reduced motion.

- [ ] **Step 3: Document implementation boundaries**

Separate map rendering, trust presentation, matching, evidence receipts, scan orchestration, owner workspace, identity, persistence, analytics, and accessibility services behind explicit interfaces.

### Task 6: Final manifest, archive, and Downloads delivery

**Files:**
- Create: `handoff/tools/build-package-manifest.ps1`
- Create: `PACKAGE-MANIFEST.json`
- Create: sibling archive `entrymap-build-ready-production-package.zip`
- Copy after verification: `C:\Users\merit\Downloads\entrymap-build-ready-production-package.zip`

**Interfaces:**
- Consumes: the completed package tree excluding transient work folders and ZIP files.
- Produces: a deterministic file inventory, final archive, archive SHA-256, and verified Downloads copy.

- [ ] **Step 1: Build the package manifest**

Record relative path, category, byte size, and SHA-256 for every package file except `PACKAGE-MANIFEST.json`, then add a manifest self-description field.

- [ ] **Step 2: Run the complete verification gate**

Expected: canonical brand, source-board integrity, crop parity, map XML/PNG validity, palette checks, reference checks, dimensions, and required document checks all pass.

- [ ] **Step 3: Create and audit the ZIP**

Compare every archive entry hash to the source tree, reject duplicate or unsafe paths, and confirm the archive entry count.

- [ ] **Step 4: Copy to Downloads and verify parity**

Copy the audited archive to the explicitly requested Downloads path and require the Downloads SHA-256 to equal the source ZIP SHA-256.
