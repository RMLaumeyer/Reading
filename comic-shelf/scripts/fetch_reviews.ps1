$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$matches = Get-Content (Join-Path $projectRoot 'data/review-matches.json') -Raw | ConvertFrom-Json
foreach ($entry in $matches.PSObject.Properties) {
    $destination = Join-Path $projectRoot ('data/cache/review-' + $entry.Name + '.html')
    if (Test-Path $destination) { continue }
    if ($entry.Name -eq '9781302940669') { Copy-Item (Join-Path $projectRoot 'data/cache/review-midnight.html') $destination; continue }
    Start-Sleep -Seconds 2
    try { Invoke-WebRequest -Uri ('https://comicbookroundup.com/comic-books/trades/marvel-comics/' + $entry.Value) -OutFile $destination -TimeoutSec 30; Write-Output ('Saved review ' + $entry.Name) }
    catch { Write-Output ('Skipped review ' + $entry.Name + ': ' + $_.Exception.Message); if ($_.Exception.Response.StatusCode.value__ -in @(401,403,429)) { break } }
}
