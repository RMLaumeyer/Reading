@echo off
cd /d "%~dp0comic-shelf"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "scripts\stop.ps1"
if errorlevel 1 pause
