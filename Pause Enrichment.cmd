@echo off
cd /d "%~dp0comic-shelf"
powershell.exe -NoProfile -Command "Set-Content -LiteralPath 'data/pause-enrichment' -Value 'pause'"
echo Enrichment will pause after the current request. Completed work is saved.
