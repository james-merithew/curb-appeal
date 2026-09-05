# Data model

## Core relationships

```text
Business 1 ── * Entrance 1 ── * FeatureClaim
                         ├── * EvidenceReceipt ── * EvidenceSource
                         ├── * CorrectionSuggestion
                         ├── * ScanSession
                         └── 0..1 approved OwnerClaim per managing account

AccessibilityProfile + Entrance claims → MatchResult
Evidence sources + owner attestation → TrustTier
Evidence observation dates → Freshness
Independent source agreement → Confidence
```

## Non-negotiable separations

- `trustTier` has exactly `Estimated`, `Scanned on-site`, and `Owner-confirmed`.
- `matchResult` has `good`, `partial`, and `unknown`; it never changes trust color or tier.
- `freshness` describes elapsed time, not entrance quality.
- `confidence` represents evidence strength and independent agreement; it is not a legal conclusion.
- `provenance` identifies who or what supplied evidence. Texas/public records are provenance only.
- `selected`, `clustered`, and `mapContext` are presentation state, not stored trust properties.
- Feature claims use only visually observed labels. Legal-compliance fields and “ADA compliant” copy are excluded.

## Trust derivation

- An entrance without an on-site photo receipt may be Estimated.
- A completed community scan with a usable source photo may upgrade it to Scanned on-site.
- An accepted owner attestation may upgrade it to Owner-confirmed while retaining community and public-record provenance.
- New evidence may refresh or correct claims, but pins never visually downgrade into a negative state. Conflicts remain visible through receipts and correction workflows.

The machine-readable schemas and enums are in `data-contracts.json`.
