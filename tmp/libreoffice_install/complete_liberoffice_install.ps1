$ErrorActionPreference = 'Stop'

$jobName = 'LibreOffice 26.2.5 MSI'
$downloadPath = Join-Path $PSScriptRoot 'LibreOffice_26.2.5_Win_x86-64.msi'
$statusPath = Join-Path $PSScriptRoot 'installation_status.log'
$msiLogPath = Join-Path $PSScriptRoot 'msiexec.log'
$expectedSha256 = 'F15BA07BFCB018698698317106350EF5D207C11F8CC051860D135271E97945F9'

function Write-Status([string]$message) {
    "$(Get-Date -Format o) $message" | Add-Content -LiteralPath $statusPath -Encoding utf8
}

try {
    $job = Get-BitsTransfer | Where-Object { $_.DisplayName -eq $jobName } | Select-Object -First 1
    if (-not $job) { throw "BITS job not found: $jobName" }

    while ($job.JobState -in @('Connecting', 'Transferring', 'Queued', 'Suspended')) {
        Write-Status "Download state=$($job.JobState) bytes=$($job.BytesTransferred)/$($job.BytesTotal)"
        Start-Sleep -Seconds 30
        $job = Get-BitsTransfer -Id $job.JobId
    }

    if ($job.JobState -ne 'Transferred') {
        throw "BITS job ended in state $($job.JobState): $($job.ErrorDescription)"
    }

    Complete-BitsTransfer -BitsJob $job
    $actualSha256 = (Get-FileHash -LiteralPath $downloadPath -Algorithm SHA256).Hash
    if ($actualSha256 -ne $expectedSha256) {
        throw "SHA-256 mismatch. Expected $expectedSha256 but received $actualSha256"
    }

    Write-Status 'Download verified. Starting silent MSI installation.'
    $installer = Start-Process -FilePath 'msiexec.exe' -ArgumentList @('/i', $downloadPath, '/qn', '/norestart', '/L*V', $msiLogPath) -WindowStyle Hidden -PassThru -Wait
    if ($installer.ExitCode -notin @(0, 3010)) {
        throw "MSI installation failed with exit code $($installer.ExitCode)."
    }

    $sofficePath = 'C:\Program Files\LibreOffice\program\soffice.exe'
    if (-not (Test-Path -LiteralPath $sofficePath)) {
        throw 'MSI exited successfully but soffice.exe was not found.'
    }
    $version = & $sofficePath --version
    Write-Status "SUCCESS: $version"
} catch {
    Write-Status "FAIL: $($_.Exception.Message)"
    exit 1
}
