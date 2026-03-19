$logDir = "C:\AI\Tutor\logs\commands"

if (!(Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir
}

$session = Get-Date -Format "yyyyMMdd_HHmmss"
$logFile = "$logDir\session_$session.log"

Register-EngineEvent PowerShell.OnCommandExecuted -Action {
    $command = $Event.SourceEventArgs.Command.CommandText
    $time = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

    "$time | $command" | Out-File -Append $logFile
}