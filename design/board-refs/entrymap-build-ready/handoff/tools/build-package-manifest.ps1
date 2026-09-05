param([Parameter(Mandatory = $true)][string]$PackageRoot)

$ErrorActionPreference = 'Stop'
$root = [System.IO.Path]::GetFullPath($PackageRoot)
$manifestPath = Join-Path $root 'PACKAGE-MANIFEST.json'
$excluded = @('PACKAGE-MANIFEST.json')

$files = Get-ChildItem -LiteralPath $root -Recurse -File | Where-Object {
  $relative = [System.IO.Path]::GetRelativePath($root,$_.FullName).Replace('\','/')
  $relative -notin $excluded -and $relative -notlike 'map-kit/.render-work/*' -and $_.Extension -ne '.zip'
} | Sort-Object FullName

$entries = foreach ($file in $files) {
  $relative = [System.IO.Path]::GetRelativePath($root,$file.FullName).Replace('\','/')
  $top = ($relative -split '/')[0]
  $category = if ($relative -match '^0[1-7]-') { 'approved-board' }
    elseif ($top -eq 'asset-library') { 'asset-library' }
    elseif ($top -eq 'screen-exports') { 'screen-export' }
    elseif ($top -eq 'map-kit') { 'map-kit' }
    elseif ($top -eq 'handoff') { 'implementation-handoff' }
    else { 'package-guide' }
  [ordered]@{
    path = $relative
    category = $category
    bytes = $file.Length
    sha256 = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash
  }
}

$manifest = [ordered]@{
  package = 'EntryMap build-ready production handoff'
  version = '2026-09-05'
  manifestRule = 'Entries cover every packaged file except PACKAGE-MANIFEST.json itself and ZIP archives.'
  entryCount = @($entries).Count
  totalBytes = ($files | Measure-Object Length -Sum).Sum
  entries = @($entries)
}
$manifest | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $manifestPath -Encoding utf8
[pscustomobject]@{ Result = 'PASS'; Entries = $manifest.entryCount; TotalBytes = $manifest.totalBytes; Manifest = $manifestPath } | Format-List
