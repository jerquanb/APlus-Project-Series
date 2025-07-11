# Storage Analyzer (PowerShell)

## 📚 CompTIA A+ 220-1201 Objectives:
- **3.4**: Compare and contrast storage devices.
- **5.2**: Troubleshoot drive and RAID issues.

---

## 🧠 Description

This script identifies the **current system drive** (where Windows is installed) and outputs the following:

- Operating system name, version, and architecture
- Drive letter and volume label
- Drive type (SSD vs HDD)
- File system format (e.g., NTFS)
- Partition style (MBR or GPT)
- Total capacity and available space
- Volume health status
- BitLocker protection status (if supported)
- OS install date (if available)

---

## 💻 Tools Used

- PowerShell 5.1+
- `Get-Volume`, `Get-PhysicalDisk`, `Get-Disk`
- `Get-CimInstance` for OS details

---

## 🧠 What I Learned

- How to detect and analyze Windows storage volumes using PowerShell
- Differences between SSDs, file systems, and partition styles
- How to simulate real-world Tier 1 diagnostics aligned with A+ exam objectives

This project replicates a help desk technician’s role in identifying drive performance issues and verifying storage configurations on a Windows-based system.
