# Storage Analyzer (PowerShell)

## 📚 CompTIA A+ 220-1201 Objectives Covered:
- **3.4**: Compare and contrast storage devices.
- **5.2**: Troubleshoot drive and RAID issues.

---

## 🧠 Description

A PowerShell script that detects and reports all storage devices on a Windows machine, including:

- Drive type (HDD, SSD, NVMe)
- File system (NTFS, exFAT, etc.)
- Total size, used space, and free space
- Partition count

---

## 💻 Tools Used

- PowerShell 5.1+
- `Get-PhysicalDisk`
- `Get-Volume`
- `Get-Disk`

---

## 🔧 Skills Demonstrated

- Windows storage management
- Command-line scripting
- Troubleshooting disk issues
- Output formatting and logging

---

## 📝 Output Sample

```powershell
Drive C: - SSD - NTFS - 500GB Total - 420GB Used - 80GB Free
Drive D: - HDD - exFAT - 1TB Total - 150GB Used - 850GB Free

