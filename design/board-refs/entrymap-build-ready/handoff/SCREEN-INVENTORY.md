# Screen inventory

The 25 reference images in `screen-exports/png` are pixel-faithful crops from the six immutable flow boards. A crop is a visual reference, not editable source code.

| Screen ID | Surface | Role | Purpose | Primary route |
|---|---|---|---|---|
| onboarding-welcome | Screen | Everyone | Explain the product; sign in or continue as guest | `/welcome` |
| onboarding-location | Screen | Everyone | Explain and request location access | `/setup/location` |
| onboarding-needs | Screen | Everyone | Set or skip optional needs | `/setup/needs` |
| profile-public | Screen | Public | Manage needs, location, display, privacy, and sign-in | `/profile` |
| map-default | Screen | Public | Explore the universal map and trust legend | `/map` |
| map-filters | Bottom sheet | Public | Filter by needs, features, freshness, distance, and open status | `/map?sheet=filters` |
| map-filtered-results | Screen | Public | Review matched pins and nearby places | `/map?filtered=true` |
| business-evidence | Bottom sheet | Public | Inspect one entrance’s trust, claims, and provenance | `/business/:businessId/entrance/:entranceId` |
| evidence-receipt | Receipt | Public | Inspect source, date, method, witnesses, and record lines | `/entrance/:entranceId/evidence/:receiptId` |
| scan-primer | Screen | Contributor | Explain the seven-second entrance scan before permission | `/scan` |
| scan-camera | Screen | Contributor | Frame and photograph the full doorway and approach | `/scan/camera` |
| scan-processing | State | Contributor | Show truthful progress events while processing | `/scan/processing/:sessionId` |
| scan-published | Bottom sheet | Contributor | Review confirmed chips and published pin | `/scan/result/:sessionId` |
| map-empty-area | State | Public | Invite the first scan or another search area | `/map?state=empty` |
| correction-form | Screen | Public | Suggest a factual correction with optional photo | `/entrance/:entranceId/correction` |
| evidence-recheck | Bottom sheet | Public | Explain aging evidence and invite a new scan | `/entrance/:entranceId/recheck` |
| system-controls | State | Public | Recover from offline, camera-off, or location-off conditions | `/system/help` |
| owner-claim-entry | Screen | Owner | Enter owner tools from Profile and start a claim | `/profile/owner` |
| owner-find-business | Screen | Owner | Find the exact business entrance to manage | `/owner/claim/find` |
| owner-confirm-ownership | Screen | Owner | Provide role, work contact, method, and authorization | `/owner/claim/confirm` |
| owner-claim-submitted | State | Owner | Track submitted, matched, and review stages | `/owner/claim/status/:claimId` |
| owner-workspace | Screen | Owner | Review one claimed entrance, freshness, confidence, and sources | `/owner/entrances/:entranceId` |
| owner-edit-entrance | Screen | Owner | Update only visible entrance observations | `/owner/entrances/:entranceId/edit` |
| owner-photos | Screen | Owner | Add, replace, remove, review, and publish entrance photos | `/owner/entrances/:entranceId/photos` |
| owner-update-receipt | Receipt | Owner | Show the published owner update and stacked provenance | `/owner/entrances/:entranceId/update/:updateId` |

Bottom navigation has three peers: Map, Scan, and Profile. Public accessibility needs are filters within the universal public experience. Owner functionality begins inside Profile after the person chooses “For business owners”; it is not a separate app.
