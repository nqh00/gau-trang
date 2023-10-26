$rclonePath = "rclone.exe"
$urlFile = "url.txt"

$urls = Get-Content $urlFile
$destination = "onedrive:"

$parallelProcesses = 10

$processes = @()

foreach ($url in $urls) {
    $arguments = "copyurl `"$url`" `"$destination`" -a -v --no-clobber"
    $process = Start-Process -NoNewWindow -FilePath $rclonePath -ArgumentList $arguments -PassThru
    $processes += $process

    while ($processes.Count -ge $parallelProcesses) {
        $runningProcesses = $processes | Where-Object { $_.HasExited -eq $false }
        $processes = $runningProcesses
        Start-Sleep -Milliseconds 100
    }
}

$processes | ForEach-Object { $_.WaitForExit() }
