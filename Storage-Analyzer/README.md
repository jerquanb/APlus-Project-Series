# ===========================
# Reliable Miracle - Storage Analyzer
# CompTIA A+ 220-1201 Objectives: 3.4, 5.2
# ===========================

# Get Operating System Info
$os = Get-CimInstance Win32_OperatingSystem
Write-Host "============================"
Write-Host "🖥️  Operating System Info"
Write-Host "============================"
Write-Host "OS: $($os.Caption) $($os.Version)"
Write-Host "Architecture: $($os.OSArchitecture)"
Write-Host "Install Date: $([Management.ManagementDateTimeConverter]::ToDateTime($os.InstallDate))"
Write-Host ""

# Get system drive letter
$sysDrive = $env:SystemDrive.TrimEnd(":")
$volume = Get-Volume -DriveLetter $sysDrive
$disk = Get-PhysicalDisk | Where-Object { $_.DeviceId -eq $volume.Path.Split("\\")[-1] -or $_.FriendlyName -ne $null } | Select-Object -First 1
$partition = Get-Disk | Where-Object { $_.Number -eq $volume.ObjectId.Split("\")[1] }

Write-Host "============================"
Write-Host "💽  System Drive Info"
Write-Host "============================"
Write-Host "Drive Letter: $($volume.DriveLetter):"
Write-Host "Volume Label: $($volume.FileSystemLabel)"
Write-Host "Drive Type: $($disk.MediaType)"
Write-Host "File System: $($volume.FileSystem)"
Write-Host "Partition Style: $($partition.PartitionStyle)"
Write-Host "Health Status: $($volume.HealthStatus)"
Write-Host ("Total Size: {0} GB" -f [math]::Round($volume.Size / 1GB, 2))
Write-Host ("Free Space: {0} GB" -f [math]::Round($volume.SizeRemaining / 1GB, 2))

# Optional BitLocker Status
try {
    $bitLocker = Get-BitLockerVolume -MountPoint "$($volume.DriveLetter):"
    if ($bitLocker) {
        Write-Host "BitLocker Status: $($bitLocker.ProtectionStatus)"
    } else {
        Write-Host "BitLocker Status: Not Enabled"
    }
} catch {
    Write-Host "BitLocker Status: Unknown or Not Supported"
}
