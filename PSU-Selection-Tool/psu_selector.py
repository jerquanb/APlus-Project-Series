import cpuinfo
import psutil
import subprocess

# === DETECTION FUNCTIONS ===

def detect_drive_count():
    drives = psutil.disk_partitions()
    return len([d for d in drives if 'cdrom' not in d.opts and d.fstype != ''])

def detect_cpu():
    info = cpuinfo.get_cpu_info()
    return info.get('brand_raw', 'Unknown CPU')

def estimate_cpu_tier(cpu_name):
    name = cpu_name.lower()
    if "i3" in name or "ryzen 3" in name:
        return "low"
    elif "i5" in name or "ryzen 5" in name:
        return "mid"
    elif "i7" in name or "ryzen 7" in name:
        return "high"
    elif "i9" in name or "ryzen 9" in name or "xeon" in name or "threadripper" in name:
        return "high"
    else:
        return "mid"

def detect_gpu():
    try:
        output = subprocess.check_output("wmic path win32_VideoController get name", shell=True)
        gpus = output.decode().strip().split('\n')[1:]
        gpus = [g.strip() for g in gpus if g.strip()]
        return gpus[0] if gpus else "None"
    except:
        return "Unknown"

def estimate_gpu_tier(gpu_name):
    name = gpu_name.lower()
    if any(x in name for x in ["1050", "rx 550", "integrated", "uhd", "vega 8"]):
        return "low"
    elif any(x in name for x in ["1660", "2060", "3060", "6600", "arc a770"]):
        return "mid"
    elif any(x in name for x in ["3080", "3090", "4080", "4090", "7900"]):
        return "enthusiast"
    elif "intel" in name and not "arc" in name:
        return "none"
    else:
        return "mid"

def is_laptop():
    battery = psutil.sensors_battery()
    return battery is not None

# === POWER ESTIMATION ===

def estimate_power(cpu_tier, gpu_tier, num_drives, cooling_type="air", laptop=False):
    if laptop:
        cpu_watts = {"low": 15, "mid": 25, "high": 45}.get(cpu_tier, 25)
        gpu_watts = {"none": 0, "low": 25, "mid": 50, "enthusiast": 100}.get(gpu_tier, 25)
    else:
        cpu_watts = {"low": 65, "mid": 95, "high": 125}.get(cpu_tier, 95)
        gpu_watts = {"none": 0, "low": 75, "mid": 150, "enthusiast": 350}.get(gpu_tier, 0)

    drive_watts = num_drives * 10
    cooling_watts = 30 if cooling_type == "liquid" else 10
    total = cpu_watts + gpu_watts + drive_watts + cooling_watts
    return total, int(total * 1.3)

def suggest_efficiency(wattage):
    if wattage >= 750:
        return "80 Plus Gold or Platinum"
    elif wattage >= 550:
        return "80 Plus Bronze or Gold"
    else:
        return "80 Plus Bronze"

def get_region_vac(region):
    if region.lower() in ["us", "usa"]:
        return "110–120 VAC"
    elif region.lower() in ["eu", "europe", "uk"]:
        return "220–240 VAC"
    else:
        return "100–240 VAC (auto-switching recommended)"

# === MAIN ===

def main():
    print("=== PSU SELECTION TOOL (Smart Version) ===")

    region = input("Enter your region (US / EU / Other): ")

    # Auto-detect hardware
    cpu_name = detect_cpu()
    cpu_tier = estimate_cpu_tier(cpu_name)
    gpu_name = detect_gpu()
    gpu_tier = estimate_gpu_tier(gpu_name)
    drive_count = detect_drive_count()
    laptop_mode = is_laptop()

    # Estimate power
    draw, recommended = estimate_power(cpu_tier, gpu_tier, drive_count, laptop=laptop_mode)
    efficiency = suggest_efficiency(recommended)
    vac_info = get_region_vac(region)

    # Output
    print("\n--- PSU RECOMMENDATION ---")
    print(f"System Type: {'Laptop' if laptop_mode else 'Desktop'}")
    print(f"Region VAC Compatibility: {vac_info}")
    print(f"Detected CPU: {cpu_name} ({cpu_tier.capitalize()} tier)")
    print(f"Detected GPU: {gpu_name} ({gpu_tier.capitalize()} tier)")
    print(f"Detected Drives: {drive_count}")
    print(f"Estimated Power Draw: {draw}W")
    print(f"Recommended PSU Wattage: {recommended}W (with 30% headroom)")
    print(f"Efficiency Rating Suggestion: {efficiency}")

    if laptop_mode:
        print("Modularity: Not applicable (laptops use internal PSUs or adapters)")
    else:
        print("Modularity: Modular recommended for airflow and cable management")

    print("\nThis PSU recommendation is based on your system’s hardware and ensures power stability, thermal efficiency, and regional compatibility.")

if __name__ == "__main__":
    main()
