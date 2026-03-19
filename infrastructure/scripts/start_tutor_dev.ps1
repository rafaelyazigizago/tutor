Write-Host "Starting Tutor AIOS Development Environment"

cd C:\AI\Tutor

Write-Host "Starting filesystem watcher..."
Start-Process python infrastructure\telemetry\file_watcher.py

Write-Host "Starting command logger..."
. infrastructure\telemetry\command_logger.ps1

Write-Host "Tutor development environment ready"