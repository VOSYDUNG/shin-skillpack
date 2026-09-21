<#
.SYNOPSIS
    Package the skill pack into dist/nnc-skillpack-<version>-<date>.zip

.DESCRIPTION
    Rebuilds portable/ from plugins/, regenerates SHA256SUMS.txt, then zips
    everything except dist/, .git/ and Python caches.

.EXAMPLE
    .\tools\make_zip.ps1
    .\tools\make_zip.ps1 -SkipBuild
#>
[CmdletBinding()]
param(
    [switch]$SkipBuild,
    [string]$Version = '1.0.0'
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root

try {
    if (-not $SkipBuild) {
        Write-Host 'Rebuilding portable bundles...' -ForegroundColor Cyan
        python tools/build_portable.py
        if ($LASTEXITCODE -ne 0) { throw "build_portable.py exited with $LASTEXITCODE" }
    }

    # --- checksums -------------------------------------------------------
    Write-Host 'Writing SHA256SUMS.txt...' -ForegroundColor Cyan
    $skip = '\\(dist|\.git|__pycache__)\\'
    $lines = Get-ChildItem -Recurse -File -Force |
        Where-Object { $_.FullName -notmatch $skip -and $_.Name -ne 'SHA256SUMS.txt' } |
        ForEach-Object {
            $rel = $_.FullName.Substring($root.Length + 1).Replace('\', '/')
            '{0}  {1}' -f (Get-FileHash $_.FullName -Algorithm SHA256).Hash.ToLower(), $rel
        }
    $lines | Sort-Object -Property { ($_ -split '  ', 2)[1] } |
        Set-Content -Path 'SHA256SUMS.txt' -Encoding utf8
    Write-Host "  $($lines.Count) files hashed"

    # --- stage and zip ---------------------------------------------------
    $stamp   = Get-Date -Format 'yyyy-MM-dd'
    $name    = "nnc-skillpack-$Version-$stamp"
    $distDir = Join-Path $root 'dist'
    $staging = Join-Path $distDir $name
    $zipPath = Join-Path $distDir "$name.zip"

    if (-not (Test-Path $distDir)) { New-Item -ItemType Directory -Path $distDir | Out-Null }
    if (Test-Path $staging) { Remove-Item -Recurse -Force $staging }
    if (Test-Path $zipPath) { Remove-Item -Force $zipPath }
    New-Item -ItemType Directory -Path $staging | Out-Null

    Write-Host 'Staging...' -ForegroundColor Cyan
    foreach ($item in '.claude-plugin', 'plugins', 'portable', 'platforms', 'tools',
                      'README.md', 'NOTICE.md', 'LICENSE', 'SHA256SUMS.txt', '.gitignore') {
        $src = Join-Path $root $item
        if (Test-Path $src) {
            Copy-Item -Recurse -Force $src -Destination (Join-Path $staging $item)
        }
    }
    Get-ChildItem -Recurse -Force -Directory $staging |
        Where-Object { $_.Name -eq '__pycache__' } |
        Remove-Item -Recurse -Force

    Write-Host 'Compressing...' -ForegroundColor Cyan
    Compress-Archive -Path (Join-Path $staging '*') -DestinationPath $zipPath -CompressionLevel Optimal
    Remove-Item -Recurse -Force $staging

    $sizeKb = [math]::Round((Get-Item $zipPath).Length / 1KB)
    Write-Host ''
    Write-Host "Done: $zipPath ($sizeKb KB)" -ForegroundColor Green
}
finally {
    Pop-Location
}
