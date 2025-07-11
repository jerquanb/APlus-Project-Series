# ===========================
# Storage Analyzer for A+ 220-1201
# Covers Objective 2.4 and more
# ===========================

# --- Operating System Info ---
$os = Get-CimInstance Win32_OperatingSystem
Write-Host "`n=== Operating System ==="
Write-Host "OS: $($os.Caption) $($os.Version)"
Write-Host "Architecture: $($os.OSArchitecture)"
if ($os.InstallDate) {
    try {
        $installDate = [Management.ManagementDateTimeConverter]::ToDateTime($os.InstallDate)
        Write-Host "Install Date: $installDate"
    } catch {
        Write-Host "Install Date: Unavailable"
    }
} else {
    Write-Host "Install Date: Unavailable"
}

# --- Storage Devices ---
Write-Host "`n=== Storage Devices ==="
$drives = Get-PhysicalDisk
foreach ($drive in $drives) {
    Write-Host "`n--- Drive: $($drive.FriendlyName) ---"
    Write-Host "Media Type: $($drive.MediaType)"
    Write-Host "Bus Type: $($drive.BusType)"
    $sizeGB = [math]::Round($drive.Size / 1GB, 2)
    Write-Host "Spindle Speed: $($drive.SpindleSpeed) RPM"
    Write-Host "Size: $sizeGB GB"

    # Form Factor Guess (only works for common combos)
    if ($drive.BusType -eq "NVMe") {
        Write-Host "Form Factor: M.2 NVMe"
    } elseif ($drive.Size -lt 600GB) {
        Write-Host "Form Factor: Likely 2.5-inch"
    } else {
        Write-Host "Form Factor: Likely 3.5-inch"
    }

    Write-Host "Health: $($drive.HealthStatus)"

    # Comparison Tip
    if ($drive.BusType -eq "NVMe") {
        Write-Host "Note: NVMe drives are the fastest consumer drives available."
    } elseif ($drive.BusType -eq "SATA") {
        Write-Host "Note: SATA SSDs are a good balance of speed and compatibility."
    } elseif ($drive.MediaType -eq "HDD") {
        Write-Host "Note: HDDs offer more storage at a lower price but are much slower."
    }
}

# --- Removable Storage ---
Write-Host "`n=== Removable Drives ==="
$removables = Get-Volume | Where-Object { $_.DriveType -eq 'Removable' }
if ($removables) {
    foreach ($rem in $removables) {
        Write-Host "Drive: $($rem.DriveLetter): - $($rem.FileSystemLabel)"
    }
} else {
    Write-Host "No removable drives detected."
}

# --- Optical Drives ---
Write-Host "`n=== Optical Drives ==="
$optical = Get-WmiObject Win32_CDROMDrive
if ($optical) {
    foreach ($cd in $optical) {
        Write-Host "Optical Drive Found: $($cd.Name)"
    }
} else {
    Write-Host "No optical drives found."
}

# --- RAID Check ---
Write-Host "`n=== RAID Check ==="
try {
    $raid = Get-StoragePool
    foreach ($r in $raid) {
        Write-Host "Pool: $($r.FriendlyName), Health: $($r.HealthStatus)"
    }
} catch {
    Write-Host "RAID info unavailable or not configured."
}

# --- A+ Study Fact ---
Write-Host "`n=== A+ Study Fact ==="
$fact = "2.5-inch drives are standard in laptops, 3.5-inch drives in desktops. RAID 1 mirrors data for fault tolerance."
Write-Host "Tip: $fact"

# --- Optional Quiz ---
$quizMode = Read-Host "`nWould you like to try a quiz question? (y/n)"
if ($quizMode -eq 'y') {
    Write-Host "`nQuestion: Which RAID level offers striping with parity?"
    $answer = Read-Host "Your answer (0, 1, 5, 6, or 10)"
   switch ($answer) {
    '5' { Write-Host "Correct! RAID 5 provides fault tolerance using parity." }
    default { Write-Host "Incorrect. The correct answer is RAID 5." }
	}
}
