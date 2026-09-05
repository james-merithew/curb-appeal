param(
  [Parameter(Mandatory = $true)][string]$PackageRoot,
  [string]$ChromePath = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$root = [System.IO.Path]::GetFullPath($PackageRoot)
$manifestPath = Join-Path $root 'map-kit/map-kit-manifest.json'
$outputRoot = Join-Path $root 'map-kit/png'
$work = Join-Path $root 'map-kit/.render-work'
if (-not (Test-Path -LiteralPath $ChromePath)) { throw "Chrome not found: $ChromePath" }
$manifest = Get-Content -Raw -LiteralPath $manifestPath | ConvertFrom-Json
New-Item -ItemType Directory -Path $outputRoot -Force | Out-Null
New-Item -ItemType Directory -Path $work -Force | Out-Null

foreach ($variant in $manifest.variants) {
  $source = Join-Path $root $variant.svg
  $output = Join-Path $root $variant.png
  $profile = Join-Path $work $variant.id
  New-Item -ItemType Directory -Path $profile -Force | Out-Null
  $url = 'file:///' + ($source -replace '\\','/')
  $args = @(
    '--headless=new','--no-sandbox','--disable-gpu-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader',
    '--hide-scrollbars','--no-first-run','--allow-file-access-from-files',"--user-data-dir=$profile",'--window-size=1170,800',
    "--screenshot=$output",$url
  )
  $process = Start-Process -FilePath $ChromePath -ArgumentList $args -WindowStyle Hidden -Wait -PassThru
  if ($process.ExitCode -ne 0 -or -not (Test-Path -LiteralPath $output)) { throw "Map render failed: $($variant.id)" }
  $image = [System.Drawing.Image]::FromFile($output)
  try {
    if ($image.Width -ne 1170 -or $image.Height -ne 800) { throw "Wrong map PNG dimensions: $($variant.id)" }
  } finally { $image.Dispose() }
  $variant | Add-Member -NotePropertyName width -NotePropertyValue 1170 -Force
  $variant | Add-Member -NotePropertyName height -NotePropertyValue 800 -Force
  $variant | Add-Member -NotePropertyName sha256 -NotePropertyValue ((Get-FileHash -LiteralPath $output -Algorithm SHA256).Hash) -Force
}

$manifest | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $manifestPath -Encoding utf8
if (Test-Path -LiteralPath $work) { Remove-Item -LiteralPath $work -Recurse -Force -ErrorAction SilentlyContinue }
[pscustomobject]@{ Result = 'PASS'; MapPngs = @($manifest.variants).Count } | Format-List
