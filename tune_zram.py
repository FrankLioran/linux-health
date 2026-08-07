# tune_zram.py
import subprocess
import sys
from config import SafetyLevel

TITLE = "ZRAM activeren"
DESCRIPTION = "Maakt een gecomprimeerde RAM-schijf aan voor swap. Dit maakt je systeem sneller als het geheugen bijna vol is."

REQUIRED_SAFETY = SafetyLevel.SAFE

def apply_fix() -> bool:
    print("\n--- ZRAM Optimalisatie ---")
    print("ZRAM maakt een gecomprimeerd RAM-geheugen aan dat fungeert als supersnelle swap.")
    print("Dit voorkomt dat je SSD gebruikt wordt bij piekbelastingen.\n")

    choice = input("ZRAM-configuratie installeren en activeren? [y/N]: ").strip().lower()
    if choice == 'y':
        try:
            print("Pakketlijst bijwerken en zram-config installeren...")
            subprocess.run(["sudo", "apt", "update"], check=True)
            subprocess.run(["sudo", "apt", "install", "-y", "zram-config"], check=True)
            print("✓ ZRAM is succesvol geïnstalleerd en geactiveerd!")
            return True
        except subprocess.CalledProcessError:
            print("✗ Er is iets misgegaan bij het installeren. Controleer je internetverbinding en sudo-rechten.")
            return False
    else:
        print("Geannuleerd.")
        return False