#memory.py
from pathlib import Path
from base import CheckCategory, CheckItem, Status

def check_memory() -> tuple[CheckCategory, int]:
    cat = CheckCategory(name="Memory")
    score_deduction = 0

    # 1. Swappiness check
    swappiness_path = Path("/proc/sys/vm/swappiness")
    if swappiness_path.exists():
        swappiness = int(swappiness_path.read_text().strip())
        if swappiness > 20:
            cat.items.append(CheckItem("Swappiness", Status.WARN, f"Swappiness = {swappiness} (aanbevolen <= 20)"))
            score_deduction += 10
        else:
            cat.items.append(CheckItem("Swappiness", Status.OK, f"Swappiness = {swappiness}"))

    # 2. ZRAM check
    zram_active = Path("/sys/block/zram0").exists()
    if zram_active:
        cat.items.append(CheckItem("ZRAM", Status.OK, "ZRAM actief"))
    else:
        cat.items.append(CheckItem("ZRAM", Status.WARN, "ZRAM niet actief"))
        score_deduction += 5

    return cat, score_deduction