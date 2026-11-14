#Requires -Version 7
<#
Weekly guard: disable GitHub Actions on any repository that should not run workflows
(forks you have not committed to, and stale repositories). Runs locally, so it costs no
Actions minutes. State and logs live in %LOCALAPPDATA%\actions-guard.

Register once:
    pwsh -File scripts/actions_guard.ps1 -Register
#>
param([switch]$Register)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$script = Join-Path $PSScriptRoot 'actions_audit.py'
$state = Join-Path $env:LOCALAPPDATA 'actions-guard'

if ($Register) {
    $action = New-ScheduledTaskAction -Execute (Get-Command pwsh).Source `
        -Argument "-NoProfile -WindowStyle Hidden -File `"$PSCommandPath`""
    $trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Saturday -At 10am
    $settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 3)
    Register-ScheduledTask -TaskName 'GitHub Actions guard' -Action $action -Trigger $trigger `
        -Settings $settings -Description 'Disables Actions on unmaintained forks and repositories' -Force | Out-Null
    Write-Output 'Registered scheduled task "GitHub Actions guard" (Saturdays 10:00).'
    return
}

$run = Join-Path $state (Get-Date -Format 'yyyy-MM-dd')
New-Item -ItemType Directory -Force $run | Out-Null
$env:GH_TOKEN = gh auth token
try {
    uv run --no-project python -X utf8 $script plan $run *> (Join-Path $run 'plan.log')
    uv run --no-project python -X utf8 $script apply $run *> (Join-Path $run 'apply.log')
}
finally {
    Remove-Item Env:GH_TOKEN -ErrorAction SilentlyContinue
}
