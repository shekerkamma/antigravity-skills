# Cross-platform porting script for Windows hosts
$skills = @(
    'book-to-skill',
    'deepgrid-architecture',
    'deepgrid-datasheet-qfn64',
    'deepgrid-dg32-2dom',
    'deepgrid-dg32-lite-ai',
    'deepgrid-dshot-bidir',
    'deepgrid-mature-silicon',
    'deepgrid-sku-compendium'
)
$srcBase = (Get-Item '.agents\skills').FullName

$userProfile = $env:USERPROFILE
$winTargets = @(
    (Join-Path $userProfile '.claude\skills'),
    (Join-Path $userProfile '.agents\skills'),
    (Join-Path $userProfile '.copilot\skills'),
    (Join-Path $userProfile '.config\agents\skills'),
    (Join-Path $userProfile '.hermes\skills'),
    (Join-Path $userProfile '.gemini\config\skills'),
    (Join-Path (Get-Location).Path '.agent\skills'),
    (Join-Path (Get-Location).Path '.claude\skills'),
    (Join-Path (Get-Location).Path '.github\skills')
)

foreach ($target in $winTargets) {
    if (!(Test-Path $target)) {
        New-Item -ItemType Directory -Force -Path $target | Out-Null
    }
    foreach ($s in $skills) {
        $sSrc = Join-Path $srcBase $s
        $sDst = Join-Path $target $s
        if (Test-Path $sSrc) {
            Copy-Item -Recurse -Force $sSrc $sDst
            Write-Host "Copied $s to $target"
        }
    }
}
Write-Host "Windows porting completed successfully."
