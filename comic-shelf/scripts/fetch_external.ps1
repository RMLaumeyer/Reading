$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$pilot = Get-Content (Join-Path $projectRoot 'data/pilot.json') -Raw | ConvertFrom-Json
$cache = Join-Path $projectRoot 'data/cache'
foreach ($url in $pilot.reviewSeries) {
    $slug = $url.Split('/')[-1]
    $destination = Join-Path $cache ('series-' + $slug + '.html')
    if (Test-Path $destination) { continue }
    Start-Sleep -Seconds 2
    try { Invoke-WebRequest -Uri $url -OutFile $destination -TimeoutSec 30; Write-Output ('Saved review series ' + $slug) }
    catch { Write-Output ('Skipped review series ' + $slug + ': ' + $_.Exception.Message); if ($_.Exception.Response.StatusCode.value__ -in @(401,403,429)) { break } }
}
foreach ($isbn in $pilot.isbns) {
    $destination = Join-Path $cache ('google-' + $isbn + '.html')
    if (Test-Path $destination) { continue }
    Start-Sleep -Seconds 2
    try { Invoke-WebRequest -Uri ('https://books.google.com/books?vid=ISBN' + $isbn) -OutFile $destination -TimeoutSec 30; Write-Output ('Saved Google Books ' + $isbn) }
    catch { Write-Output ('Skipped Google Books ' + $isbn + ': ' + $_.Exception.Message); if ($_.Exception.Response.StatusCode.value__ -in @(401,403,429)) { break } }
}
