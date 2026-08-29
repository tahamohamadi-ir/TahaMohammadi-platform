# Promote owner-local design intake into tracked frontend-design-authority.
# Usage (from workspace root):
#   pwsh scripts/promote-design-intake.ps1
#   pwsh scripts/promote-design-intake.ps1 -WhatIf

param(
    [switch]$WhatIf
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$srcRoot = Join-Path $root "Front-End\Assets"
$dstRoot = Join-Path $root "Docs\references\frontend-design-authority"

$syncDirs = @(
    "agent-kit",
    "concepts",
    "art",
    "brand"
)

if (-not (Test-Path $srcRoot)) {
    Write-Error "Source not found: $srcRoot"
}

function Copy-IfDifferent([string]$relativePath) {
    $src = Join-Path $srcRoot $relativePath
    $dst = Join-Path $dstRoot $relativePath
    if (-not (Test-Path $src)) { return }
    $dstDir = Split-Path $dst -Parent
    if (-not (Test-Path $dstDir)) {
        if ($WhatIf) { Write-Host "[WhatIf] mkdir $dstDir"; return }
        New-Item -ItemType Directory -Path $dstDir -Force | Out-Null
    }
    $srcHash = (Get-FileHash $src -Algorithm SHA256).Hash
    $dstHash = if (Test-Path $dst) { (Get-FileHash $dst -Algorithm SHA256).Hash } else { $null }
    if ($srcHash -eq $dstHash) {
        Write-Host "skip (unchanged): $relativePath"
        return
    }
    if ($WhatIf) {
        Write-Host "[WhatIf] copy $relativePath"
        return
    }
    Copy-Item $src $dst -Force
    Write-Host "promoted: $relativePath"
}

Write-Host "Promoting from $srcRoot -> $dstRoot"
foreach ($dir in $syncDirs) {
    $full = Join-Path $srcRoot $dir
    if (-not (Test-Path $full)) { continue }
    Get-ChildItem $full -Recurse -File | ForEach-Object {
        $rel = $_.FullName.Substring($srcRoot.Length + 1)
        Copy-IfDifferent $rel
    }
}

if ($WhatIf) {
    Write-Host "WhatIf complete. Run without -WhatIf to apply, then regenerate SHA256SUMS and run validate.mjs."
    exit 0
}

$validator = Join-Path $dstRoot "agent-kit\validate.mjs"
if (Test-Path $validator) {
    Write-Host "Running design authority validator..."
    node $validator
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

Write-Host "Promotion complete. Update SHA256SUMS.txt if binary files changed (validator may report drift)."
