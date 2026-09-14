$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$pilot = Get-Content (Join-Path $projectRoot 'data/pilot.json') -Raw | ConvertFrom-Json
$catalog = Get-Content (Join-Path $projectRoot 'public/catalog.json') -Raw | ConvertFrom-Json
$cache = Join-Path $projectRoot 'data/cache'
$records = @($catalog.books | Where-Object { $_.isbn -in $pilot.isbns })
if ($records.Count -ne $pilot.isbns.Count) { throw 'A pilot ISBN did not match exactly one catalog record.' }
foreach ($book in $records) {
    $destination = Join-Path $cache ($book.isbn + '.html')
    if (Test-Path -LiteralPath $destination) { continue }
    if ($book.isbn -eq '9781302940669' -and (Test-Path (Join-Path $cache 'midnight.html'))) {
        Copy-Item -LiteralPath (Join-Path $cache 'midnight.html') -Destination $destination
        continue
    }
    if (([uri]$book.catalogUrl).Host -ne 'catalog.ocls.org') { throw 'Unexpected catalog host' }
    # Respect OCLS's published 20-second crawl delay. Cache avoids repeat requests.
    Start-Sleep -Seconds 20
    try {
        Invoke-WebRequest -Uri $book.catalogUrl -OutFile $destination -TimeoutSec 30
        Write-Output ('Saved ' + $book.title)
    } catch {
        Write-Output ('Skipped ' + $book.isbn + ': ' + $_.Exception.Message)
        if ($_.Exception.Response.StatusCode.value__ -in @(401,403,429)) { break }
    }
}
