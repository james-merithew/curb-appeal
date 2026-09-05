param([Parameter(Mandatory = $true)][string]$PackageRoot)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$root = [System.IO.Path]::GetFullPath($PackageRoot)
$specPath = Join-Path $root 'screen-exports/screen-export-spec.json'
$outputRoot = Join-Path $root 'screen-exports/png'
$manifestPath = Join-Path $root 'screen-exports/screen-export-manifest.json'

if (-not (Test-Path -LiteralPath $specPath)) { throw "Crop specification not found: $specPath" }
$spec = Get-Content -Raw -LiteralPath $specPath | ConvertFrom-Json
New-Item -ItemType Directory -Path $outputRoot -Force | Out-Null

foreach ($existing in Get-ChildItem -LiteralPath $outputRoot -File -Filter '*.png' -ErrorAction SilentlyContinue) {
  Remove-Item -LiteralPath $existing.FullName -Force
}

$exports = [System.Collections.Generic.List[object]]::new()
foreach ($screen in $spec.screens) {
  $sourcePath = Join-Path $root $screen.source
  if (-not (Test-Path -LiteralPath $sourcePath)) { throw "Missing source board: $($screen.source)" }
  $source = [System.Drawing.Bitmap]::FromFile($sourcePath)
  try {
    if ($source.Width -ne [int]$spec.sourceCanvas.width -or $source.Height -ne [int]$spec.sourceCanvas.height) {
      throw "Unexpected source dimensions for $($screen.source): $($source.Width)x$($source.Height)"
    }
    $rectangle = [System.Drawing.Rectangle]::new([int]$screen.x, [int]$screen.y, [int]$screen.width, [int]$screen.height)
    if ($rectangle.Left -lt 0 -or $rectangle.Top -lt 0 -or $rectangle.Right -gt $source.Width -or $rectangle.Bottom -gt $source.Height) {
      throw "Crop is outside source bounds: $($screen.id)"
    }
    $crop = $source.Clone($rectangle, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
    try {
      $fileName = "$($screen.id).png"
      $outputPath = Join-Path $outputRoot $fileName
      $crop.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Png)
      $hash = (Get-FileHash -LiteralPath $outputPath -Algorithm SHA256).Hash
      $exports.Add([ordered]@{
        id = $screen.id
        kind = $screen.kind
        path = "screen-exports/png/$fileName"
        source = $screen.source
        crop = [ordered]@{ x = [int]$screen.x; y = [int]$screen.y; width = [int]$screen.width; height = [int]$screen.height }
        width = $crop.Width
        height = $crop.Height
        sha256 = $hash
      })
    } finally { $crop.Dispose() }
  } finally { $source.Dispose() }
}

$manifest = [ordered]@{
  version = 1
  method = $spec.method
  sourceCanvas = $spec.sourceCanvas
  count = $exports.Count
  screens = $exports
}
$manifest | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $manifestPath -Encoding utf8
[pscustomobject]@{ Result = 'PASS'; ScreenExports = $exports.Count; Manifest = $manifestPath } | Format-List
