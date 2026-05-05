[CmdletBinding()]
param(
    [switch]$Force,
    [switch]$SkipSmokeTests
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
$Provisioner = Join-Path $ScriptDir "provision_demo_env.py"

function Test-PythonCandidate {
    param(
        [string]$Command,
        [string[]]$Arguments
    )

    $resolved = Get-Command $Command -ErrorAction SilentlyContinue
    if ($resolved -and $resolved.Source -like "*\WindowsApps\python*.exe") {
        return $false
    }

    if ((Test-Path $Command) -or $resolved) {
        & $Command @Arguments --version *> $null
        if ($LASTEXITCODE -eq 0) {
            return $true
        }
    }

    return $false
}

$candidates = @(
    @{ Command = (Join-Path $RepoRoot ".venv\Scripts\python.exe"); Arguments = @() },
    @{ Command = "py"; Arguments = @("-3") },
    @{ Command = "python"; Arguments = @() },
    @{ Command = "python3"; Arguments = @() },
    @{ Command = "C:\Program Files\Blender Foundation\Blender 5.0\5.0\python\bin\python.exe"; Arguments = @() }
)

$selected = $null
foreach ($candidate in $candidates) {
    if (Test-PythonCandidate -Command $candidate.Command -Arguments $candidate.Arguments) {
        $selected = $candidate
        break
    }
}

if (-not $selected) {
    Write-Error "Python 3.11+ was not found. Install Python, then rerun .\demos\provision_demo_env.ps1."
    exit 1
}

$provisionArgs = @()
$provisionArgs += $selected.Arguments
$provisionArgs += $Provisioner

if ($Force) {
    $provisionArgs += "--force"
}

if ($SkipSmokeTests) {
    $provisionArgs += "--skip-smoke-tests"
}

Push-Location $RepoRoot
try {
    & $selected.Command @provisionArgs
    exit $LASTEXITCODE
}
finally {
    Pop-Location
}
