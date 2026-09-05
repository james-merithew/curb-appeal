# Engineering handoff

## Recommended modules

| Module | Owns | Must not own |
|---|---|---|
| `identity` | guest/account session and sign-in return path | trust computation or map rendering |
| `profiles` | optional needs and local/account storage | trust-tier filtering |
| `map` | provider camera, clustering, overlays, nearby list | evidence truth or owner authorization |
| `trust` | fixed tier derivation and upgrade events | matching, freshness, selection, or clustering |
| `matching` | profile-to-claim good/partial/unknown result | pin tier or confidence |
| `evidence` | claims, receipts, sources, freshness, confidence, corrections | legal-compliance conclusions |
| `scan` | permission primer, camera, processing events, review, offline queue | fabricated progress or owner confirmation |
| `owner` | claim workflow, scoped workspace, observations, photos | editing public/state records |
| `accessibility` | focus, announcements, reduced motion, text scaling | business rules |
| `analytics` | stable events from `FLOW-MATRIX.csv` | source photos or sensitive free text by default |

## Suggested interfaces

```ts
type TrustTier = 'Estimated' | 'Scanned on-site' | 'Owner-confirmed';
type MatchResult = 'good' | 'partial' | 'unknown';
type MapContext = 'overview' | 'street' | 'selected' | 'receipt' | 'live-scan';

interface TrustPresentation {
  tier: TrustTier;
  mapContext: MapContext;
  assetId: 'estimated' | 'scanned-on-site' | 'owner-confirmed';
  sizePx: number;
}

interface EntranceOverlayState {
  match?: MatchResult;
  selected: boolean;
  freshnessState: 'current' | 'aging' | 'recheck';
  clustered: boolean;
}

interface ScanProgressEvent {
  sessionId: string;
  step: 'Doorway framed' | 'Entry path visible' | 'Entrance features checked' | 'Photo quality checked';
  completedAt: string;
}
```

## Build order

1. Implement design tokens, accessible controls, and the fixed trust-pin renderer.
2. Implement the universal map shell, nearby list, filters, sheets, and evidence receipts using fixture data.
3. Add optional needs profiles and independent match halos.
4. Add corrections and the scan state machine with offline queue and reduced motion.
5. Add authentication boundaries and owner claim/workspace routes.
6. Connect persistent APIs and analytics after the fixture-driven UI satisfies acceptance checks.

## Acceptance gates

- Every route/action in `FLOW-MATRIX.csv` is implemented or explicitly feature-flagged off.
- Every rendered trust pin matches the fixed wording, icon, color, ring completion, and context size.
- Trust, matching, freshness, confidence, provenance, selection, and clustering can change independently in component tests.
- Guest exploration works without sign-in; pending contribution returns correctly after authentication.
- Receipts always expose provenance and Suggest a correction.
- Owner edits cannot mutate community or public/state evidence rows.
- Camera, location denial, empty results, offline queue, aging evidence, and reduced motion pass device tests.
- Body contrast targets 7:1 and all controls meet the 48 px minimum.

The visual crops establish appearance. The CSV/JSON files establish behavior and data. When they appear to conflict, fixed trust wording and immutable brand rules take precedence, then `FLOW-MATRIX.csv`, then the explanatory Markdown.
