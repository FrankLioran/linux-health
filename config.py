#config.py
from enum import IntEnum
from pathlib import Path

class SafetyLevel(IntEnum):
    CHECK_ONLY = 1
    SAFE = 2
    ADVANCED = 3
    EXPERT = 4

# Paden
REPORTS_DIR = Path.home() / "HealthReports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)