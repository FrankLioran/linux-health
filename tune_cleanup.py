# tune_cleanup.py
import shutil
import subprocess
from config import SafetyLevel

TITLE = "Systeem & Docker Opruimen"
DESCRIPTION = "Verwijdert ongebruikte Docker-containers/images en verouderde pakket-caches om schijfruimte te winnen."

REQUIRED_SAFETY = SafetyLevel.SAFE

def apply_fix() -> bool:
    print("\n--- Systeem Opruimen ---")
    print("Dit verwijdert ongebruikte Docker-containers/images en verouderde pakket-caches.\n")

    choice = input("Schoonmaak uitvoeren? [y/N]: ").strip().lower()
    if choice == 'y':
        try:
            print("1. Apt pakket-cache opschonen...")
            subprocess.run(["sudo", "apt", "autoremove", "-y"], check=True)
            subprocess.run(["sudo", "apt", "clean"], check=True)

            if shutil.which("docker"):
                print("2. Docker prune uitvoeren...")
                subprocess.run(["docker", "system", "prune", "-f"], check=True)

            print("✓ Systeem succesvol opgeruimd!")
            return True
        except Exception as e:
            print(f"✗ Fout tijdens opschonen: {e}")
            return False
    return False