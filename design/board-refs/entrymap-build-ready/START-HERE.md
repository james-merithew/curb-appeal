# Start here: EntryMap build-ready production handoff

This package contains the approved presentation boards, immutable brand sources, individual screen references, reusable UI/pin assets, demo-map layers, interaction rules, and implementation mappings for the universal public experience and authenticated owner workspace.

## Fast path by role

### Product and UX

1. Read `BUILD-READY-HANDOFF-DESIGN.md`.
2. Review `handoff/SCREEN-INVENTORY.md`, `handoff/ROUTE-MAP.md`, and `handoff/FLOW-MAP.md`.
3. Use `handoff/FLOW-MATRIX.csv` and `handoff/SCREEN-STATE-MATRIX.csv` as the detailed behavior checklist.

### Visual and interaction design

1. Treat `07-entrymap-approved-logo.png` and `asset-library/canonical-brand/*` as immutable.
2. Review the six root flow boards and the 25 separate references in `screen-exports/png`.
3. Use `asset-library/entrymap-asset-catalog.png`, `asset-library/asset-manifest.json`, and `asset-library/tokens`.
4. Use `map-kit` for editable demo-map compositions and `asset-library/INTERACTION-MOTION-SPEC.md` for motion.

### Engineering

1. Start with `handoff/ENGINEERING-HANDOFF.md` and `handoff/MAP-IMPLEMENTATION.md`.
2. Implement screens and routes from `handoff/SCREEN-INVENTORY.md` and `handoff/FLOW-MATRIX.csv`.
3. Map components using `handoff/COMPONENT-MATRIX.csv` and data using `handoff/data-contracts.json`.
4. Validate with `handoff/ACCESSIBILITY-CHECKLIST.md` and `handoff/RESPONSIVE-SPEC.md`.

## Package boundaries

- Included: 25 separate approved-screen crops, three trust pins in SVG/PNG sizes, evidence hierarchy, match halos, clusters, UI components/states, provenance including Texas records, eight vector/raster demo maps, routes, flows, data contracts, responsive rules, accessibility, and engineering guidance.
- Not included: production application code, backend services, authentication provider, scanning/vision model, geographic database, navigation/routing data, proprietary map tiles, or legal determinations.
- The demo-map files are design references and prototype assets; a shipping app must connect them to a real map provider and entrance dataset.

## Fixed trust ladder

1. Estimated — hollow dashed sky pin, italic information symbol, zero of three evidence segments.
2. Scanned on-site — solid marigold pin, person symbol, two of three evidence segments.
3. Owner-confirmed — solid violet pin, storefront symbol, three of three evidence segments, separate outlined check.

Pins only upgrade. Trust is never a filter. Texas records are provenance only. Never use a shield, red, gray, legal-compliance language, or the word “verified” for owners.

`PACKAGE-MANIFEST.json` contains the final file inventory and hashes. Run `handoff/tools/verify-build-ready-handoff.ps1 -PackageRoot <folder>` to audit the unpacked package.
