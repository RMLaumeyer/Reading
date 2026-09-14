$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$pidFile = Join-Path $projectRoot '.panel.pid'
if (-not (Test-Path $pidFile)) { Write-Output 'Panel is not running from this launcher.'; exit }
$panelProcessId = [int](Get-Content $pidFile -Raw)
$process = Get-CimInstance Win32_Process -Filter ('ProcessId = ' + $panelProcessId)
$serverPath = Join-Path $projectRoot 'scripts/serve.mjs'
if ($process -and $process.Name -eq 'node.exe' -and $process.CommandLine.Contains($serverPath)) {
    $panelProcess = [System.Diagnostics.Process]::GetProcessById($panelProcessId)
    $panelProcess.Kill()
    $panelProcess.WaitForExit()
    Write-Output 'Panel stopped.'
} elseif ($process) { throw 'The saved process no longer belongs to Panel. Nothing was stopped.' }
Remove-Item -LiteralPath $pidFile
