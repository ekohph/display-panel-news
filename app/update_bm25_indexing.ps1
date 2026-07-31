<#
.SYNOPSIS
Rebuild the persisted BM25 index from summaries, trends, and panel-pricing-research.

.EXAMPLE
.\app\update_bm25_indexing.ps1

.EXAMPLE
.\app\update_bm25_indexing.ps1 -PythonExe .\.venv\Scripts\python.exe
#>

[CmdletBinding()]
param(
    [string]$PythonExe = "python"
)

$ErrorActionPreference = "Stop"
$scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
$indexBuilder = Join-Path $scriptDirectory "build_index.py"

if (-not (Test-Path -LiteralPath $indexBuilder -PathType Leaf)) {
    throw "BM25 index builder was not found: $indexBuilder"
}

& $PythonExe $indexBuilder
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
