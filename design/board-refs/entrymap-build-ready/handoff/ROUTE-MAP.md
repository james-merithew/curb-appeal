# Route map

```text
App launch
├─ First use → /welcome
│  ├─ Sign in → system-auth → /setup/location
│  └─ Continue as guest → /setup/location
├─ Setup
│  ├─ /setup/location → system location permission → /setup/needs
│  └─ /setup/needs → choose or skip → /map
└─ Returning use → /map

/map
├─ Filters sheet → filtered results → selected entrance
├─ Empty area → scan an entrance | try another area
├─ Selected entrance → business/evidence sheet
│  ├─ Feature/evidence badge → evidence receipt
│  ├─ Suggest a correction → correction form
│  └─ Aging evidence → re-check sheet → scan camera
├─ Scan tab → primer → camera → processing → published result → map
└─ Profile tab
   ├─ Public profile and needs
   └─ For business owners
      ├─ Claim your door → find → confirm → status
      └─ Claimed entrance workspace
         ├─ Edit entrance → review/publish → update receipt
         ├─ Manage photos → review/publish → update receipt
         └─ View public listing → selected entrance
```

## Authentication boundaries

- Map browsing, temporary needs filters, entrance details, receipts, and empty-area exploration work as a guest.
- Sign-in is requested only to sync a profile, save places, submit a scan/correction, or begin an owner claim.
- If sign-in is required mid-flow, preserve the pending action and return to the originating screen afterward.
- Owner routes require an authenticated account. Workspace routes additionally require an approved owner claim for that entrance.

## Navigation rules

- Map, Scan, and Profile are peer destinations and crossfade over 180 ms.
- Business sheets, receipts, correction forms, setup, and owner tools are hierarchical destinations and transition over 260 ms.
- Closing a sheet returns focus to the opening pin or control.
- Back from processing is unavailable after upload begins; “Keep exploring” leaves an offline scan safely queued.
- Operating-system permission surfaces are external routes named `os-location-permission`, `os-camera-permission`, and `os-settings` in the flow matrix.
