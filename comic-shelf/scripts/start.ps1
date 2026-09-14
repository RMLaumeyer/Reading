param([switch]$NoBrowser)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$url = 'http://127.0.0.1:5173/'
$healthUrl = 'http://127.0.0.1:5173/health'
$running = $false
try { $health = Invoke-RestMethod $healthUrl -TimeoutSec 2; $running = $health.app -eq 'panel-comic-shelf' } catch { }
if (-not $running) {
    $bundledNode = Join-Path $env:USERPROFILE '.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe'
    if (Test-Path $bundledNode) { $nodeExe=$bundledNode } else { $nodeExe=(Get-Command node -ErrorAction Stop).Source }
    $serverPath = Join-Path $projectRoot 'scripts/serve.mjs'
    $process = Start-Process -FilePath $nodeExe -ArgumentList ('"' + $serverPath + '"') -WorkingDirectory $projectRoot -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $projectRoot 'panel.log') -RedirectStandardError (Join-Path $projectRoot 'panel-error.log')
    Set-Content (Join-Path $projectRoot '.panel.pid') $process.Id
    for ($attempt=0;$attempt -lt 20;$attempt++) {
        Start-Sleep -Milliseconds 250
        try { $health = Invoke-RestMethod $healthUrl -TimeoutSec 2; if ($health.app -eq 'panel-comic-shelf') { $running=$true;break } } catch { }
        if ($process.HasExited) { break }
    }
    if (-not $running) { throw 'Panel could not start. Check comic-shelf/panel-error.log; port 5173 may already be in use.' }
}
if (-not $NoBrowser) { Start-Process $url }
