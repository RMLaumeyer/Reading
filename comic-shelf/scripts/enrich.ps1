param([switch]$Retry)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$pauseFile = Join-Path $projectRoot 'data/pause-enrichment'
if (Test-Path $pauseFile) { Remove-Item -LiteralPath $pauseFile }
$pythonExe = Join-Path $env:USERPROFILE '.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
if (-not (Test-Path $pythonExe)) { $pythonExe = (Get-Command python -ErrorAction Stop).Source }
$scriptPath = Join-Path $projectRoot 'scripts/enrich_catalog.py'
$workerArguments = '"' + $scriptPath + '"'
if ($Retry) { $workerArguments += ' --retry' }
Start-Process -FilePath $pythonExe -ArgumentList $workerArguments -WorkingDirectory $projectRoot -WindowStyle Hidden -RedirectStandardOutput (Join-Path $projectRoot 'enrichment-output.log') -RedirectStandardError (Join-Path $projectRoot 'enrichment-stderr.log')
Write-Output 'Enrichment started or resumed. Progress appears in Panel. Keep this computer awake.'
