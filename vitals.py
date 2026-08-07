# vitals.py
import subprocess
import os
from base import CheckCategory, CheckItem, Status

def check_vitals() -> tuple[CheckCategory, int]:
    cat = CheckCategory(name="System Vitals")
    deduction = 0

    # Load Average (1, 5, 15 min)
    load1, load5, _ = os.getloadavg()
    cpu_count = os.cpu_count() or 1

    if load1 > cpu_count * 1.5:
        cat.items.append(CheckItem("CPU Load", Status.WARN, f"Hoge belasting: {load1:.2f} (Cores: {cpu_count})"))
        deduction += 5
    else:
        cat.items.append(CheckItem("CPU Load", Status.OK, f"Normaal ({load1:.2f})"))

    # GPU Temp (als nvidia-smi aanwezig is)
    try:
        temp = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader,nounits"],
            text=True
        ).strip()
        temp_val = int(temp)
        if temp_val > 80:
            cat.items.append(CheckItem("GPU Temp", Status.WARN, f"Warm: {temp_val}°C"))
            deduction += 10
        else:
            cat.items.append(CheckItem("GPU Temp", Status.OK, f"{temp_val}°C"))
    except Exception:
        pass  # Geen GPU of fout bij uitlezen

    return cat, deduction