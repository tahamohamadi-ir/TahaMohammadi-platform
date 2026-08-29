[CmdletBinding()]
param(
  [switch]$Execute
)

$ErrorActionPreference = 'Stop'

$authorityRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$docsRoot = (Resolve-Path (Join-Path $authorityRoot '..\..')).Path
$repoRoot = (Resolve-Path (Join-Path $docsRoot '..')).Path
$assetsRoot = Join-Path $repoRoot 'Front-End\Assets'
$inventoryPath = Join-Path $PSScriptRoot 'INCOMING-INVENTORY.json'
$deletionMapPath = Join-Path $PSScriptRoot 'DELETION-MAP.json'
$validatorPath = Join-Path $authorityRoot 'agent-kit\validate.mjs'

function Assert-UnderRoot([string]$Path, [string]$Root) {
  $fullPath = [System.IO.Path]::GetFullPath($Path)
  $fullRoot = [System.IO.Path]::GetFullPath($Root).TrimEnd('\') + '\'
  if (-not $fullPath.StartsWith($fullRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Unsafe path outside expected root: $fullPath"
  }
  return $fullPath
}

function Invoke-CheckedMove([string]$Source, [string]$Destination) {
  if (-not (Test-Path -LiteralPath $Source)) { return }
  Assert-UnderRoot $Source $assetsRoot | Out-Null
  Assert-UnderRoot $Destination $assetsRoot | Out-Null
  Write-Host "MOVE $Source -> $Destination"
  if ($Execute) {
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $Destination) | Out-Null
    Move-Item -LiteralPath $Source -Destination $Destination
  }
}

function Invoke-CheckedDelete([string]$Source) {
  if (-not (Test-Path -LiteralPath $Source)) { return }
  Assert-UnderRoot $Source $assetsRoot | Out-Null
  Write-Host "DELETE duplicate $Source"
  if ($Execute) { Remove-Item -LiteralPath $Source -Force }
}

if (-not (Test-Path -LiteralPath $assetsRoot)) { throw "Assets root missing: $assetsRoot" }
if (-not (Test-Path -LiteralPath $inventoryPath)) { throw "Inventory missing: $inventoryPath" }
if (-not (Test-Path -LiteralPath $deletionMapPath)) { throw "Deletion map missing: $deletionMapPath" }

Write-Host '1/5 Validate tracked authority before any local action.'
& node $validatorPath
if ($LASTEXITCODE -ne 0) { throw 'Tracked authority validation failed; no cleanup performed.' }

$inventory = Get-Content -LiteralPath $inventoryPath -Raw | ConvertFrom-Json
$deletionMap = Get-Content -LiteralPath $deletionMapPath -Raw | ConvertFrom-Json

Write-Host '2/5 Preserve unique incoming items in the local archive.'
foreach ($item in $inventory.files | Where-Object { $_.classification -eq 'unmanaged-unique' }) {
  $source = Join-Path $assetsRoot $item.relativePath
  $destination = Join-Path $assetsRoot (Join-Path 'archive\unmanaged-unique' $item.relativePath)
  Invoke-CheckedMove $source $destination
}
foreach ($item in $inventory.files | Where-Object { $_.relativePath -like 'assets/*' -and $_.classification -ne 'verified-duplicate' }) {
  $source = Join-Path $assetsRoot $item.relativePath
  $destination = Join-Path $assetsRoot (Join-Path 'archive\legacy-assets' $item.relativePath)
  Invoke-CheckedMove $source $destination
}

Write-Host '3/5 Preserve unique requested variants in their normalized local location.'
$variants = @(
  @{ Source = 'concepts\requested-2026-08-25\home-dark-safe-reference.png'; Destination = 'concepts\variants\home-dark-safe-reference.png' },
  @{ Source = 'concepts\requested-2026-08-25\home-light-alternate-reference.png'; Destination = 'concepts\variants\home-light-alternate-reference.png' }
)
foreach ($variant in $variants) {
  Invoke-CheckedMove (Join-Path $assetsRoot $variant.Source) (Join-Path $assetsRoot $variant.Destination)
}

Write-Host '4/5 Delete only candidates whose retained tracked authority copy has the same SHA-256.'
foreach ($entry in $deletionMap) {
  if ($entry.retained_path -notlike 'authority/*') { throw "Deletion map contains non-authority retained path: $($entry.delete_path)" }
  $source = Join-Path $assetsRoot $entry.delete_path
  $retainedRelative = $entry.retained_path.Substring('authority/'.Length).Replace('/', '\')
  $retained = Join-Path $authorityRoot $retainedRelative
  if (-not (Test-Path -LiteralPath $source)) {
    Write-Host "SKIP already-removed duplicate $source"
    continue
  }
  if (-not (Test-Path -LiteralPath $retained)) { throw "Tracked retained copy missing: $retained" }
  $sourceHash = (Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash.ToLowerInvariant()
  $retainedHash = (Get-FileHash -LiteralPath $retained -Algorithm SHA256).Hash.ToLowerInvariant()
  if ($sourceHash -ne $entry.sha256 -or $retainedHash -ne $entry.sha256) {
    throw "Hash proof failed for $($entry.delete_path)"
  }
  Invoke-CheckedDelete $source
}

$aliases = @(
  @{ Source = 'concepts\requested-2026-08-25\home-dark-final-reference.png'; Retained = 'concepts\home-dark-concept-v3-final.png' },
  @{ Source = 'concepts\requested-2026-08-25\home-light-final-reference.png'; Retained = 'concepts\home-light-concept-v3-final.png' },
  @{ Source = 'concepts\requested-2026-08-25\language-gateway-centered-dark-reference.png'; Retained = 'concepts\language-gateway-dark-concept-v1.png' }
)
foreach ($alias in $aliases) {
  $source = Join-Path $assetsRoot $alias.Source
  $retained = Join-Path $authorityRoot $alias.Retained
  if ((Test-Path -LiteralPath $source) -and (Test-Path -LiteralPath $retained)) {
    if ((Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash -ne (Get-FileHash -LiteralPath $retained -Algorithm SHA256).Hash) {
      throw "Alias hash proof failed for $($alias.Source)"
    }
    Invoke-CheckedDelete $source
  }
}

Write-Host '5/5 Preserve local package documentation, then remove only emptied legacy directories.'
$legacyDocs = @('ACCEPTANCE-GATES.md','AGENT-COORDINATION.md','design.md','DOCUMENT-MIGRATION-MAP.md','figma-lite-state.json','FRONTEND-IMPLEMENTATION-ARCHITECTURE-BLUEPRINT.md','IDEA-vision.md','MANIFEST.md','MASTER-SPEC.md','MULTI-AGENT-TASK-LIST.md','PROMPTS.md','README.md','REFERENCE-MANIFEST.json','SHA256SUMS.txt','SOURCE-INVENTORY.md','WORKTREE-SNAPSHOT.md')
foreach ($name in $legacyDocs) {
  Invoke-CheckedMove (Join-Path $assetsRoot $name) (Join-Path $assetsRoot (Join-Path 'provenance\legacy-package' $name))
}
foreach ($name in @('history','superpowers','templates')) {
  Invoke-CheckedMove (Join-Path $assetsRoot $name) (Join-Path $assetsRoot (Join-Path 'provenance\legacy-package' $name))
}

foreach ($relative in @('assets','others','concepts\requested-2026-08-25')) {
  $target = Join-Path $assetsRoot $relative
  if (Test-Path -LiteralPath $target) {
    if (-not $Execute) {
      Write-Host "VERIFY-THEN-REMOVE legacy directory after planned moves: $target"
      continue
    }
    $remainingFiles = @(Get-ChildItem -LiteralPath $target -Recurse -File -Force)
    if ($remainingFiles.Count -ne 0) { throw "Legacy directory still has files and will not be removed: $target" }
    Assert-UnderRoot $target $assetsRoot | Out-Null
    Write-Host "REMOVE empty legacy directory $target"
    if ($Execute) { Remove-Item -LiteralPath $target -Recurse -Force }
  }
}

if ($Execute) { Write-Host 'Cleanup complete.' } else { Write-Host 'Dry run complete. Re-run with -Execute only after reviewing this output.' }
