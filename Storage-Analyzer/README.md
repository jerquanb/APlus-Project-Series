# File: Get-SystemDriveInfo.ps1

$systemDrive = $env:SystemDrive.TrimEnd('\')  # e.g., "C:"
$volume = Get-Volume -DriveLetter $systemDrive.TrimEnd(':')
$partition = Get-Partition -DriveLetter $systemDrive.TrimEnd(':')
$disk = Get-Disk -Number $partition.DiskNumber
$physicalDisk = Get-PhysicalDisk | Where-Object { $_.DeviceId -eq $disk.Number }
$bitlocker = Get-BitLockerVolume -MountPoint $systemDrive -ErrorAction SilentlyContinue

Write-Host "=== System Drive Information ==="
Write-Host "Drive Letter: $($volume.DriveLetter):"
Write-Host "Label       : $($volume.FileSystemLabel)"
Write-Host "Total Size  : $([Math]::Round($volume.Size / 1GB, 2)) GB"
Write-Host "Free Space  : $([Math]::Round($volume.SizeRemaining / 1GB, 2)) GB"
Write-Host "File System : $($volume.FileSystem)"
Write-Host "Health      : $($volume.HealthStatus)"
Write-Host "Drive Type  : $($physicalDisk.MediaType)"
Write-Host "Partition Style: $($disk.PartitionStyle)"

if ($bitlocker) {
    Write-Host "BitLocker   : $($bitlocker.ProtectionStatus)"
    Write-Host "Encryption  : $($bitlocker.EncryptionMethod)"
} else {
    Write-Host "BitLocker   : Not Available or Not Enabled"
}

