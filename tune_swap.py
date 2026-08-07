# tune_swap.py
import subprocess
from pathlib import Path
from config import SafetyLevel

TITLE = "Swappiness optimaliseren"
DESCRIPTION = "Verlaagt de neiging van Linux om geheugen naar de schijf (swap) te schrijven. Aanbevolen voor SSD's en AI-workloads."

REQUIRED_SAFETY = SafetyLevel.SAFE

def apply_fix() -> bool:
    swappiness_path = Path("/proc/sys/vm/swappiness")

    # 1. Huidige waarde uitlezen
    try:
        current = swappiness_path.read_text().strip()
    except Exception:
        current = "Onbekend"

    print(f"\nHuidige swappiness: {current}")
    print("Aanbevolen waarde: 10\n")

    # 2. Gebruiker om bevestiging vragen
    choice = input("Swappiness aanpassen naar 10 (tijdelijk + permanent)? [y/N]: ").strip().lower()

    if choice == 'y':
        try:
            # 3A. Direct toepassen in het actieve geheugen
            subprocess.run(["sudo", "sysctl", "vm.swappiness=10"], check=True)

            # 3B. Permanent maken voor toekomstige herstarts
            conf_file = "/etc/sysctl.d/99-swappiness.conf"
            subprocess.run(
                ["sudo", "bash", "-c", f"echo 'vm.swappiness=10' > {conf_file}"],
                check=True
            )

            print("✓ Swappiness succesvol ingesteld op 10 (actief en permanent opgeslagen).")
            return True

        except subprocess.CalledProcessError:
            print("✗ Mislukt. Zorg dat je sudo-rechten hebt.")
            return False
        except Exception as e:
            print(f"✗ Er is een fout opgetreden: {e}")
            return False
    else:
        print("Geannuleerd. Geen wijzigingen doorgevoerd.")
        return False