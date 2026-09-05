param([Parameter(Mandatory = $true)][string]$PackageRoot)

$ErrorActionPreference = 'Stop'
$root = [System.IO.Path]::GetFullPath($PackageRoot)
$errors = [System.Collections.Generic.List[string]]::new()

function Require-File([string]$relativePath) {
  $path = Join-Path $root $relativePath
  if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { $errors.Add("Missing file: $relativePath") }
  return $path
}

function Require-Hash([string]$relativePath, [string]$expectedHash) {
  $path = Require-File $relativePath
  if (Test-Path -LiteralPath $path -PathType Leaf) {
    $actual = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash
    if ($actual -ne $expectedHash) { $errors.Add("Immutable source changed: $relativePath") }
  }
}

$immutable = [ordered]@{
  '01-onboarding-and-profile.png' = '14D458E3131BFCFB476E337935BFDD3C7A5D9118CE1CAB4F2951CFA09E7F05F6'
  '02-map-filters-and-evidence.png' = '0CBC326FF0886893498EA9B955DF73EF8FA28FB1BDE8E620D01B189194E98584'
  '03-community-scan-flow.png' = 'D0F3AEFA248774AD4DAB4F9AD8EC4DBFF7CA4A77B2DEFD20BD603018043231B4'
  '04-community-and-system-states.png' = 'A15683DD925881E3D26DABE21C8FDDE9C1A3BBAB3BAC4DFCFD36261E9C46C28E'
  '05-owner-claim-flow.png' = '386F02C00543CEBDAF9D241BFC599B9573FB32942EB041B40DAAB8CDF7A60505'
  '06-owner-workspace.png' = 'A081CF48B3B7641E4494E5BD76C333F1EF9BCA3D0CC4A8E7DA83B06A3AC7C2DF'
  '07-entrymap-approved-logo.png' = '34C82AC8D20535A16F7167F895F0D3EFB7419AF6ADA794733C7E32C9F0784B54'
  'asset-library/canonical-brand/entrymap-approved-full.png' = '34C82AC8D20535A16F7167F895F0D3EFB7419AF6ADA794733C7E32C9F0784B54'
  'asset-library/canonical-brand/entrymap-approved-header-lockup.png' = '56322AA92BAA7699F7B1169F1DFBA39B14FA82BFAEAAE76B9613897FC83A24C7'
}
foreach ($item in $immutable.GetEnumerator()) { Require-Hash $item.Key $item.Value }

$requiredDocs = @(
  'START-HERE.md',
  'handoff/SCREEN-INVENTORY.md',
  'handoff/ROUTE-MAP.md',
  'handoff/FLOW-MAP.md',
  'handoff/FLOW-MATRIX.csv',
  'handoff/SCREEN-STATE-MATRIX.csv',
  'handoff/COMPONENT-MAP.md',
  'handoff/COMPONENT-MATRIX.csv',
  'handoff/DATA-MODEL.md',
  'handoff/data-contracts.json',
  'handoff/RESPONSIVE-SPEC.md',
  'handoff/ACCESSIBILITY-CHECKLIST.md',
  'handoff/MAP-IMPLEMENTATION.md',
  'handoff/ENGINEERING-HANDOFF.md',
  'screen-exports/screen-export-manifest.json',
  'map-kit/map-kit-manifest.json',
  'map-kit/README.md',
  'PACKAGE-MANIFEST.json'
)
foreach ($relative in $requiredDocs) { [void](Require-File $relative) }

$screenManifestPath = Join-Path $root 'screen-exports/screen-export-manifest.json'
if (Test-Path -LiteralPath $screenManifestPath) {
  $screenManifest = Get-Content -Raw -LiteralPath $screenManifestPath | ConvertFrom-Json
  if (@($screenManifest.screens).Count -ne 25) { $errors.Add("Screen export count is $(@($screenManifest.screens).Count); expected 25") }
  Add-Type -AssemblyName System.Drawing
  foreach ($screen in $screenManifest.screens) {
    $path = Join-Path $root $screen.path
    if (-not (Test-Path -LiteralPath $path)) { $errors.Add("Missing screen PNG: $($screen.path)"); continue }
    $image = [System.Drawing.Image]::FromFile($path)
    try {
      if ($image.Width -ne [int]$screen.width -or $image.Height -ne [int]$screen.height) { $errors.Add("Screen dimensions do not match manifest: $($screen.id)") }
    } finally { $image.Dispose() }
    $actualHash = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash
    if ($actualHash -ne $screen.sha256) { $errors.Add("Screen hash does not match manifest: $($screen.id)") }
    $sourcePath = Join-Path $root $screen.source
    if (Test-Path -LiteralPath $sourcePath) {
      $source = [System.Drawing.Bitmap]::FromFile($sourcePath)
      try {
        $rectangle = [System.Drawing.Rectangle]::new([int]$screen.crop.x,[int]$screen.crop.y,[int]$screen.crop.width,[int]$screen.crop.height)
        $crop = $source.Clone($rectangle,[System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
        try {
          $tempCrop = Join-Path ([System.IO.Path]::GetTempPath()) ("entrymap-crop-{0}.png" -f ([guid]::NewGuid().ToString('N')))
          $crop.Save($tempCrop,[System.Drawing.Imaging.ImageFormat]::Png)
          try {
            if ((Get-FileHash -LiteralPath $tempCrop -Algorithm SHA256).Hash -ne $actualHash) { $errors.Add("Screen pixels do not match documented source crop: $($screen.id)") }
          } finally { Remove-Item -LiteralPath $tempCrop -Force -ErrorAction SilentlyContinue }
        } finally { $crop.Dispose() }
      } finally { $source.Dispose() }
    }
  }
}

$mapIds = @('base-map','before-profile','after-profile','selected-business','empty-area','mixed-cluster','pin-placement','safe-areas')
foreach ($id in $mapIds) {
  $svg = Join-Path $root "map-kit/svg/$id.svg"
  $png = Join-Path $root "map-kit/png/$id.png"
  if (-not (Test-Path -LiteralPath $svg)) { $errors.Add("Missing map SVG: $id") } else {
    try {
      $xml = [xml](Get-Content -Raw -LiteralPath $svg)
      if ($xml.svg.viewBox -ne '0 0 1170 800') { $errors.Add("Wrong map viewBox: $id") }
    } catch { $errors.Add("Invalid map SVG XML: $id") }
  }
  if (-not (Test-Path -LiteralPath $png)) { $errors.Add("Missing map PNG: $id") }
}

$mapManifestPath = Join-Path $root 'map-kit/map-kit-manifest.json'
if (Test-Path -LiteralPath $mapManifestPath) {
  $mapManifest = Get-Content -Raw -LiteralPath $mapManifestPath | ConvertFrom-Json
  if (@($mapManifest.variants).Count -ne 8) { $errors.Add("Map manifest count is $(@($mapManifest.variants).Count); expected 8") }
  Add-Type -AssemblyName System.Drawing
  foreach ($variant in $mapManifest.variants) {
    $png = Join-Path $root $variant.png
    if (-not (Test-Path -LiteralPath $png)) { continue }
    $image = [System.Drawing.Bitmap]::FromFile($png)
    try {
      if ($image.Width -ne 1170 -or $image.Height -ne 800) { $errors.Add("Wrong map PNG dimensions: $($variant.id)") }
      $visible = $false
      for ($y = 0; $y -lt $image.Height -and -not $visible; $y += 8) {
        for ($x = 0; $x -lt $image.Width; $x += 8) { if ($image.GetPixel($x,$y).A -gt 0) { $visible = $true; break } }
      }
      if (-not $visible) { $errors.Add("Fully transparent map PNG: $($variant.id)") }
    } finally { $image.Dispose() }
    if (-not $variant.sha256) { $errors.Add("Map hash missing from manifest: $($variant.id)") }
    elseif ((Get-FileHash -LiteralPath $png -Algorithm SHA256).Hash -ne $variant.sha256) { $errors.Add("Map hash mismatch: $($variant.id)") }
  }
}

$forbidden = '#17103D|#5B35F5|#69B7FF|#FFBF24|Nunito Sans|const logoMark|const wordmark'
$textFiles = Get-ChildItem -LiteralPath $root -Recurse -File -Include '*.svg','*.css','*.json','*.md','*.mjs' |
  Where-Object { $_.Name -notin @('verify-canonical-brand.ps1','verify-build-ready-handoff.ps1') }
$matches = @($textFiles | Select-String -Pattern $forbidden -CaseSensitive:$false)
if ($matches.Count -gt 0) { $errors.Add("Forbidden reconstructed-brand or substitute-palette references: $($matches.Count)") }

if ((Test-Path -LiteralPath (Join-Path $root 'handoff/FLOW-MATRIX.csv')) -and (Test-Path -LiteralPath (Join-Path $root 'screen-exports/screen-export-manifest.json'))) {
  $screens = @((Get-Content -Raw -LiteralPath (Join-Path $root 'screen-exports/screen-export-manifest.json') | ConvertFrom-Json).screens.id)
  $flows = Import-Csv -LiteralPath (Join-Path $root 'handoff/FLOW-MATRIX.csv')
  foreach ($flow in $flows) {
    foreach ($field in @('from_screen','to_screen')) {
      $value = $flow.$field
      if ($value -and $value -notin $screens -and $value -notlike 'os-*' -and $value -notlike 'system-*') { $errors.Add("Unresolved $field '$value' in flow $($flow.step_id)") }
    }
  }
}

if ((Test-Path -LiteralPath (Join-Path $root 'handoff/SCREEN-STATE-MATRIX.csv')) -and $screens) {
  $states = Import-Csv -LiteralPath (Join-Path $root 'handoff/SCREEN-STATE-MATRIX.csv')
  if (@($states).Count -ne 25) { $errors.Add("Screen-state row count is $(@($states).Count); expected 25") }
  foreach ($state in $states) { if ($state.screen_id -notin $screens) { $errors.Add("Unknown screen in state matrix: $($state.screen_id)") } }
}

if ((Test-Path -LiteralPath (Join-Path $root 'handoff/COMPONENT-MATRIX.csv')) -and $screens) {
  $assetManifest = Get-Content -Raw -LiteralPath (Join-Path $root 'asset-library/asset-manifest.json') | ConvertFrom-Json
  $assetKeys = @($assetManifest.assets | ForEach-Object { "$($_.category)/$($_.id)" })
  $components = Import-Csv -LiteralPath (Join-Path $root 'handoff/COMPONENT-MATRIX.csv')
  foreach ($component in $components) {
    foreach ($asset in @($component.asset_ids -split ';')) {
      if ($asset -notin $assetKeys -and $asset -notlike 'canonical-brand/*') { $errors.Add("Unknown asset '$asset' in component $($component.component)") }
    }
    if ($component.owning_screens -ne 'all screens') {
      foreach ($screen in @($component.owning_screens -split ';')) { if ($screen -notin $screens) { $errors.Add("Unknown owner screen '$screen' in component $($component.component)") } }
    }
  }
}

$contractsPath = Join-Path $root 'handoff/data-contracts.json'
if (Test-Path -LiteralPath $contractsPath) {
  $contracts = Get-Content -Raw -LiteralPath $contractsPath | ConvertFrom-Json
  $tiers = @($contracts.'$defs'.TrustTier.enum)
  if (($tiers -join '|') -ne 'Estimated|Scanned on-site|Owner-confirmed') { $errors.Add('TrustTier enum does not match the fixed ladder.') }
  $features = @($contracts.'$defs'.FeatureName.enum)
  if ($features.Count -ne 7) { $errors.Add("FeatureName enum count is $($features.Count); expected 7") }
}

$packageManifestPath = Join-Path $root 'PACKAGE-MANIFEST.json'
if (Test-Path -LiteralPath $packageManifestPath) {
  $packageManifest = Get-Content -Raw -LiteralPath $packageManifestPath | ConvertFrom-Json
  $expectedFiles = @(Get-ChildItem -LiteralPath $root -Recurse -File | Where-Object {
    $relative = [System.IO.Path]::GetRelativePath($root,$_.FullName).Replace('\','/')
    $relative -ne 'PACKAGE-MANIFEST.json' -and $relative -notlike 'map-kit/.render-work/*' -and $_.Extension -ne '.zip'
  })
  if ([int]$packageManifest.entryCount -ne $expectedFiles.Count) { $errors.Add("Package manifest count is $($packageManifest.entryCount); expected $($expectedFiles.Count)") }
  $listedPaths = @($packageManifest.entries.path)
  foreach ($file in $expectedFiles) {
    $relative = [System.IO.Path]::GetRelativePath($root,$file.FullName).Replace('\','/')
    $entry = $packageManifest.entries | Where-Object path -eq $relative
    if (-not $entry) { $errors.Add("Package manifest missing: $relative"); continue }
    if ([long]$entry.bytes -ne $file.Length) { $errors.Add("Package manifest size mismatch: $relative") }
    if ($entry.sha256 -ne (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash) { $errors.Add("Package manifest hash mismatch: $relative") }
  }
  foreach ($listed in $listedPaths) { if (-not (Test-Path -LiteralPath (Join-Path $root $listed))) { $errors.Add("Package manifest lists missing file: $listed") } }
}

if ($errors.Count -gt 0) {
  $errors | ForEach-Object { Write-Output "FAIL: $_" }
  throw "BUILD-READY HANDOFF: FAIL ($($errors.Count) issues)"
}

[pscustomobject]@{
  Result = 'PASS'
  ImmutableSources = $immutable.Count
  ScreenExports = 25
  MapVariants = 8
  RequiredDocuments = $requiredDocs.Count
  ForbiddenMatches = 0
} | Format-List
