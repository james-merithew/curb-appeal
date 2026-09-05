param(
  [Parameter(Mandatory = $true)][string]$SourceRoot,
  [Parameter(Mandatory = $true)][string]$WorkRoot,
  [string]$ChromePath = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$source = [System.IO.Path]::GetFullPath($SourceRoot)
$work = [System.IO.Path]::GetFullPath($WorkRoot)

if (-not (Test-Path -LiteralPath $ChromePath)) { throw "Chrome not found: $ChromePath" }
if (-not (Test-Path -LiteralPath (Join-Path $source 'asset-manifest.json'))) { throw "Asset manifest not found in: $source" }

New-Item -ItemType Directory -Path $work -Force | Out-Null
$workResolved = [System.IO.Path]::GetFullPath($work)
foreach ($folderName in @('svg', 'png', 'rendered', 'profiles', 'canonical-brand')) {
  $stale = [System.IO.Path]::GetFullPath((Join-Path $work $folderName))
  if (-not $stale.StartsWith($workResolved, [System.StringComparison]::OrdinalIgnoreCase)) { throw "Unsafe render cleanup target: $stale" }
  if ((Split-Path $stale -Leaf) -ne $folderName) { throw "Unexpected render cleanup target: $stale" }
  if (Test-Path -LiteralPath $stale) { Remove-Item -LiteralPath $stale -Recurse -Force }
}
Copy-Item -LiteralPath (Join-Path $source 'svg') -Destination $work -Recurse -Force
Copy-Item -LiteralPath (Join-Path $source 'canonical-brand') -Destination $work -Recurse -Force
Copy-Item -LiteralPath (Join-Path $source 'entrymap-asset-catalog.svg') -Destination (Join-Path $work 'entrymap-asset-catalog.svg') -Force

$manifest = Get-Content -Raw -LiteralPath (Join-Path $source 'asset-manifest.json') | ConvertFrom-Json
$plan = [System.Collections.Generic.List[object]]::new()

function Add-Export([object]$asset, [int]$width, [int]$height, [string]$suffix) {
  $inputPath = Join-Path $work ($asset.svg -replace '^asset-library/', '')
  $outputDir = Join-Path (Join-Path $work 'png') $asset.category
  $renderDir = Join-Path (Join-Path $work 'rendered') $asset.category
  New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
  New-Item -ItemType Directory -Path $renderDir -Force | Out-Null
  $outputPath = Join-Path $outputDir ("{0}-{1}.png" -f $asset.id, $suffix)
  $renderPath = Join-Path $renderDir ("{0}-{1}.png" -f $asset.id, $suffix)
  $renderScale = [int][Math]::Max(1, [Math]::Ceiling(512 / [Math]::Min($width, $height)))
  $plan.Add([pscustomobject]@{
    input = $inputPath; output = $outputPath; width = $width; height = $height
    render = $renderPath; renderWidth = ($width * $renderScale); renderHeight = ($height * $renderScale)
    category = $asset.category; id = $asset.id; size = $suffix
  })
}

foreach ($asset in $manifest.assets) {
  $parts = @($asset.viewBox -split ' ' | ForEach-Object { [double]$_ })
  $naturalW = [int]$parts[2]
  $naturalH = [int]$parts[3]
  switch ($asset.category) {
    { $_ -in @('ui-icons', 'feature-icons', 'provenance') } {
      foreach ($size in @(24, 32, 48)) { Add-Export $asset $size $size ("{0}px" -f $size) }
    }
    { $_ -in @('pins', 'halos') } {
      foreach ($height in @(48, 72, 96)) {
        $width = [int][Math]::Round($naturalW * $height / $naturalH)
        Add-Export $asset $width $height ("{0}px" -f $height)
      }
    }
    'brand' {
      if ($asset.id -eq 'favicon') {
        foreach ($size in @(32, 64)) { Add-Export $asset $size $size ("{0}px" -f $size) }
      } elseif ($asset.id -eq 'app-icon') {
        foreach ($size in @(256, 512, 1024)) { Add-Export $asset $size $size ("{0}px" -f $size) }
      } elseif ($asset.id -like 'wordmark*') {
        Add-Export $asset 520 150 '1x'
        Add-Export $asset 1040 300 '2x'
      } else {
        foreach ($scale in @(1, 2, 4)) { Add-Export $asset ($naturalW * $scale) ($naturalH * $scale) ("{0}x" -f $scale) }
      }
    }
    default {
      Add-Export $asset $naturalW $naturalH '1x'
      Add-Export $asset ($naturalW * 2) ($naturalH * 2) '2x'
    }
  }
}

$profilesRoot = Join-Path $work 'profiles'
New-Item -ItemType Directory -Path $profilesRoot -Force | Out-Null
$failures = [System.Collections.Generic.List[string]]::new()
$batchSize = 4

for ($offset = 0; $offset -lt $plan.Count; $offset += $batchSize) {
  $processes = @()
  $batchEnd = [Math]::Min($offset + $batchSize - 1, $plan.Count - 1)
  for ($i = $offset; $i -le $batchEnd; $i++) {
    $item = $plan[$i]
    $slot = $i % $batchSize
    $profile = Join-Path $profilesRoot ("worker-{0}" -f $slot)
    New-Item -ItemType Directory -Path $profile -Force | Out-Null
    $url = 'file:///' + ($item.input -replace '\\', '/')
    $args = @(
      '--headless=new', '--no-sandbox', '--disable-gpu-sandbox', '--use-angle=swiftshader',
      '--enable-unsafe-swiftshader', '--hide-scrollbars', '--no-first-run',
      '--default-background-color=00000000', "--user-data-dir=$profile",
      ("--window-size={0},{1}" -f $item.renderWidth, $item.renderHeight),
      ("--screenshot={0}" -f $item.render), $url
    )
    $processes += [pscustomobject]@{ process = (Start-Process -FilePath $ChromePath -ArgumentList $args -WindowStyle Hidden -PassThru); item = $item }
  }
  foreach ($record in $processes) {
    $record.process.WaitForExit()
    if ($record.process.ExitCode -ne 0 -or -not (Test-Path -LiteralPath $record.item.render)) {
      $failures.Add("$($record.item.category)/$($record.item.id)/$($record.item.size)")
      continue
    }
    $sourceBitmap = [System.Drawing.Bitmap]::FromFile($record.item.render)
    $targetBitmap = New-Object System.Drawing.Bitmap($record.item.width, $record.item.height, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
    $graphics = [System.Drawing.Graphics]::FromImage($targetBitmap)
    $graphics.Clear([System.Drawing.Color]::Transparent)
    $graphics.CompositingMode = [System.Drawing.Drawing2D.CompositingMode]::SourceCopy
    $graphics.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality
    $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
    $graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
    $graphics.DrawImage($sourceBitmap, 0, 0, $record.item.width, $record.item.height)
    $graphics.Dispose()
    $sourceBitmap.Dispose()
    $targetBitmap.Save($record.item.output, [System.Drawing.Imaging.ImageFormat]::Png)
    $targetBitmap.Dispose()
  }
  Write-Progress -Activity 'Exporting EntryMap PNG assets' -Status "$([Math]::Min($batchEnd + 1, $plan.Count)) of $($plan.Count)" -PercentComplete (([Math]::Min($batchEnd + 1, $plan.Count) / $plan.Count) * 100)
}

if ($failures.Count -gt 0) { throw "PNG exports failed: $($failures -join ', ')" }

$catalogOut = Join-Path $work 'entrymap-asset-catalog.png'
$catalogUrl = 'file:///' + ((Join-Path $work 'entrymap-asset-catalog.svg') -replace '\\', '/')
$catalogSource = Get-Content -Raw -LiteralPath (Join-Path $work 'entrymap-asset-catalog.svg')
if ($catalogSource -notmatch 'viewBox="0 0 ([0-9]+) ([0-9]+)"') { throw 'Could not read catalog viewBox.' }
$catalogWidth = [int]$Matches[1]
$catalogHeight = [int]$Matches[2]
$catalogArgs = @('--headless=new','--no-sandbox','--disable-gpu-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader','--hide-scrollbars','--no-first-run','--allow-file-access-from-files',"--user-data-dir=$(Join-Path $profilesRoot 'catalog')",("--window-size={0},{1}" -f $catalogWidth,$catalogHeight),"--screenshot=$catalogOut",$catalogUrl)
$catalogProcess = Start-Process -FilePath $ChromePath -ArgumentList $catalogArgs -WindowStyle Hidden -Wait -PassThru
if ($catalogProcess.ExitCode -ne 0 -or -not (Test-Path -LiteralPath $catalogOut)) { throw 'Catalog PNG export failed.' }

New-Item -ItemType Directory -Path (Join-Path $source 'png') -Force | Out-Null
Copy-Item -Path (Join-Path $work 'png\*') -Destination (Join-Path $source 'png') -Recurse -Force
Copy-Item -LiteralPath $catalogOut -Destination (Join-Path $source 'entrymap-asset-catalog.png') -Force

$exportManifest = [pscustomobject]@{
  generated = (Get-Date).ToUniversalTime().ToString('o')
  count = $plan.Count
  exports = @($plan | ForEach-Object {
    [pscustomobject]@{
      category = $_.category
      id = $_.id
      size = $_.size
      width = $_.width
      height = $_.height
      png = ('png/{0}/{1}' -f $_.category, [System.IO.Path]::GetFileName($_.output))
    }
  })
}
$exportManifest | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $source 'png-export-manifest.json') -Encoding utf8

[pscustomobject]@{ SvgMasters = $manifest.assets.Count; PngExports = $plan.Count; Catalog = 'entrymap-asset-catalog.png' }
