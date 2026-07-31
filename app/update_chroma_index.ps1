[CmdletBinding()]
param(
    [string]$Python = "",
    [switch]$Reset,
    [ValidateRange(1, 1000)]
    [int]$BatchSize = 32
)

$ErrorActionPreference = "Stop"
$appDir = $PSScriptRoot
$scriptPath = Join-Path $appDir "update_chroma_index.py"

if (-not $Python) {
    $venvPython = Join-Path $appDir "..\.venv\Scripts\python.exe"
    $Python = if (Test-Path $venvPython) { $venvPython } else { "python" }
}

$arguments = @($scriptPath, "--batch-size", $BatchSize)
if ($Reset) {
    $arguments += "--reset"
}

& $Python @arguments
exit $LASTEXITCODE
