# Component map

## Composition

```text
AppShell
├─ AppHeader
├─ RouteContent
│  ├─ MapSurface
│  │  ├─ ProviderMap
│  │  ├─ EntrancePinLayer
│  │  ├─ MatchHaloLayer
│  │  ├─ ClusterLayer
│  │  └─ MapControls
│  ├─ BottomSheet
│  │  ├─ BusinessSummary
│  │  ├─ TrustBadge
│  │  ├─ FreshnessIndicator
│  │  ├─ ConfidenceIndicator
│  │  ├─ FeatureChipList
│  │  └─ EvidenceReceipt
│  ├─ ScanFlow
│  │  ├─ PermissionPrimer
│  │  ├─ DoorwayCamera
│  │  ├─ ScanProgress
│  │  └─ PublishReview
│  └─ OwnerWorkspace
│     ├─ OwnerClaimFlow
│     ├─ EntranceEditor
│     ├─ PhotoManager
│     └─ OwnerUpdateReceipt
└─ BottomNavigation
```

## Independence rules

- `EntrancePin` receives only trust tier and map context. It does not compute trust.
- `MatchHalo` receives match result and wraps a pin without changing it.
- `FreshnessIndicator`, `ConfidenceIndicator`, `SelectionKeyline`, and `ClusterMarker` are separate overlays.
- `EvidenceReceipt` renders source photo, observed date, method, witness/provenance lines, confidence, freshness, and correction action.
- `NeedsFilter` never accepts trust tier as an option.
- `OwnerWorkspace` may edit owner observations and photos; public/state record rows are read-only.

See `COMPONENT-MATRIX.csv` for canonical asset IDs, variants, semantic roles, and owning screens.
