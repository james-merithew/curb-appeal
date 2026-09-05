param(
  [Parameter(Mandatory = $true)][string]$PackageRoot,
  [Parameter(Mandatory = $true)][string]$ApprovedFullLogo,
  [Parameter(Mandatory = $true)][string]$ApprovedHeaderLockup
)

$ErrorActionPreference = 'Stop'
$errors = [System.Collections.Generic.List[string]]::new()
$package = [System.IO.Path]::GetFullPath($PackageRoot)
$library = Join-Path $package 'asset-library'
$canonical = Join-Path $library 'canonical-brand'

function Require-ExactCopy([string]$expected, [string]$actual, [string]$label) {
  if (-not (Test-Path -LiteralPath $actual)) { $errors.Add("Missing canonical ${label}: $actual"); return }
  $expectedHash = (Get-FileHash -LiteralPath $expected -Algorithm SHA256).Hash
  $actualHash = (Get-FileHash -LiteralPath $actual -Algorithm SHA256).Hash
  if ($expectedHash -ne $actualHash) { $errors.Add("Canonical $label was altered: $actual") }
}

Require-ExactCopy $ApprovedFullLogo (Join-Path $canonical 'entrymap-approved-full.png') 'full logo'
Require-ExactCopy $ApprovedHeaderLockup (Join-Path $canonical 'entrymap-approved-header-lockup.png') 'header lockup'
Require-ExactCopy $ApprovedFullLogo (Join-Path $package '07-entrymap-approved-logo.png') 'root approved logo'

if (Test-Path -LiteralPath (Join-Path $library 'svg\brand')) { $errors.Add('Reconstructed SVG logo directory is present.') }
if (Test-Path -LiteralPath (Join-Path $library 'png\brand')) { $errors.Add('Reconstructed PNG logo directory is present.') }

$builder = Get-Content -Raw -LiteralPath (Join-Path $package 'build-assets.mjs')
if ($builder -match 'const logoMark|const wordmark|Nunito Sans') { $errors.Add('Package builder still contains reconstructed logo or wordmark code.') }

$tokensPath = Join-Path $library 'tokens\design-tokens.json'
if (-not (Test-Path -LiteralPath $tokensPath)) {
  $errors.Add('Design tokens are missing.')
} else {
  $tokens = Get-Content -Raw -LiteralPath $tokensPath | ConvertFrom-Json
  $expected = [ordered]@{
    indigo900 = '#1E1142'
    violet600 = '#4F34DB'
    sky400 = '#76BCFD'
    marigold400 = '#FDB327'
    lavenderPath = '#CFBCEE'
  }
  foreach ($key in $expected.Keys) {
    $actual = $tokens.color.$key
    if ($actual -ne $expected[$key]) { $errors.Add("Palette mismatch for ${key}: expected $($expected[$key]), got $actual") }
  }
}

$forbiddenApproximation = '#17103D|#5B35F5|#69B7FF|#FFBF24'
$affected = @(rg -l $forbiddenApproximation (Join-Path $library 'svg') 2>$null)
if ($affected.Count -gt 0) { $errors.Add("$($affected.Count) SVG files still use substituted logo colors.") }

if ($errors.Count -gt 0) {
  Write-Host 'BRAND INTEGRITY: FAIL'
  $errors | ForEach-Object { Write-Host "- $_" }
  exit 1
}

Write-Host 'BRAND INTEGRITY: PASS'
Write-Host 'Approved logo sources are byte-identical; no reconstructed brand assets or substitute core colors remain.'
