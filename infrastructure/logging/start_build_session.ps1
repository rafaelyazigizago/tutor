Write-Host "Starting Tutor AIOS Build Session..."

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"

$logDir = "logs\build"

if (!(Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir
}

New-Item "$logDir\session_$timestamp.log"

Write-Host "Session created: $timestamp"