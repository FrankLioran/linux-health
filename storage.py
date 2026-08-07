# storage.py
import shutil
from pathlib import Path
from base import CheckCategory, CheckItem, Status

def check_storage() -> tuple[CheckCategory, int]:
    cat = CheckCategory(name="Storage & Disk Health")
    deduction = 0

    # 1. Root-partitie ruimte
    total, used, free = shutil.disk_usage("/")
    free_gb = free // (2**30)
    used_pct = (used / total) * 100

    if used_pct > 90:
        cat.items.append(CheckItem("Root Schijf", Status.FAIL, f"Kritiek: {used_pct:.1f}% gebruikt ({free_gb} GB vrij)"))
        deduction += 20
    elif used_pct > 80:
        cat.items.append(CheckItem("Root Schijf", Status.WARN, f"Let op: {used_pct:.1f}% gebruikt ({free_gb} GB vrij)"))
        deduction += 10
    else:
        cat.items.append(CheckItem("Root Schijf", Status.OK, f"{used_pct:.1f}% gebruikt ({free_gb} GB vrij)"))

    # 2. Check op herstart vereist (Ubuntu/Debian)
    if Path("/var/run/reboot-required").exists():
        cat.items.append(CheckItem("Systeem Update", Status.WARN, "Systeem vereist een herstart na updates"))
        deduction += 5
    else:
        cat.items.append(CheckItem("Systeem Update", Status.OK, "Geen herstart vereist"))

    return cat, deduction