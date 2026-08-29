param(
    [string]$WorkspaceRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..\..')).Path
)

$ErrorActionPreference = 'Stop'
$incomingRoot = Join-Path $WorkspaceRoot 'Front-End\Assets'
$authorityRoot = Split-Path -Parent $PSScriptRoot
$legacyRoot = Join-Path $WorkspaceRoot 'Docs\references\legacy-planning'
$inventoryPath = Join-Path $PSScriptRoot 'INCOMING-INVENTORY.json'
$deletionMapPath = Join-Path $PSScriptRoot 'DELETION-MAP.json'

function Get-Records([string]$Root) {
    Get-ChildItem -LiteralPath $Root -Recurse -File | ForEach-Object {
        [pscustomobject]@{
            path = $_.FullName.Substring($Root.Length).TrimStart('\').Replace('\', '/')
            sha256 = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
            bytes = $_.Length
            extension = $_.Extension.ToLowerInvariant()
        }
    }
}

$authority = @(Get-Records $authorityRoot)
$legacy = @(Get-Records $legacyRoot)
$authorityByHash = @{}
foreach ($record in $authority) {
    if (-not $authorityByHash.ContainsKey($record.sha256)) { $authorityByHash[$record.sha256] = @() }
    $authorityByHash[$record.sha256] += "authority/$($record.path)"
}
$legacyByHash = @{}
foreach ($record in $legacy) {
    if (-not $legacyByHash.ContainsKey($record.sha256)) { $legacyByHash[$record.sha256] = @() }
    $legacyByHash[$record.sha256] += "legacy/$($record.path)"
}

$items = foreach ($record in Get-Records $incomingRoot) {
    $authorityRetained = @($authorityByHash[$record.sha256] | Sort-Object)
    $legacyRetained = @($legacyByHash[$record.sha256] | Sort-Object)
    $retained = @($authorityRetained + $legacyRetained)
    $classification = if ($record.path -like 'assets/*' -and $authorityRetained.Count -gt 0) {
        'verified-duplicate'
    } elseif ($record.path -like 'others/*' -and $authorityRetained.Count -gt 0) {
        'verified-duplicate'
    } elseif ($record.path -like 'others/*') {
        'unmanaged-unique'
    } elseif ($record.path -like 'history/*' -or $record.path -like 'superpowers/*' -or $record.path -like 'templates/*' -or $record.path -in @('design.md', 'IDEA-vision.md')) {
        'history'
    } elseif ($record.path -like 'concepts/*' -or $record.path -like 'art/*' -or $record.path -like 'brand/*' -or $record.path -like 'agent-kit/*') {
        'retained-local-source'
    } else {
        'needs-review'
    }
    [pscustomobject]@{
        path = $record.path
        sha256 = $record.sha256
        bytes = $record.bytes
        extension = $record.extension
        classification = $classification
        retained_paths = $retained
        canonical_retained_paths = $authorityRetained
    }
}

$deletions = @($items | Where-Object { $_.classification -eq 'verified-duplicate' } | ForEach-Object {
    [pscustomobject]@{
        delete_path = $_.path
        sha256 = $_.sha256
        retained_path = $_.canonical_retained_paths[0]
        deletion_authorized_only_if_hash_matches = $true
    }
})

$payload = [ordered]@{
    generated_at = (Get-Date).ToUniversalTime().ToString('o')
    incoming_root = $incomingRoot
    authority_root = $authorityRoot
    file_count = @($items).Count
    unique_hash_count = @($items.sha256 | Sort-Object -Unique).Count
    total_bytes = [int64](($items.bytes | Measure-Object -Sum).Sum)
    items = $items
}
$payload | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $inventoryPath -Encoding utf8
$deletions | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $deletionMapPath -Encoding utf8

Write-Output "Wrote $inventoryPath and $deletionMapPath with $($deletions.Count) verified deletion candidates."
