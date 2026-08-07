# tune_uv.py
import subprocess
import shutil
from config import SafetyLevel

TITLE = "'uv' Python Package Manager installeren"
DESCRIPTION = "Installeert 'uv', een razendsnelle vervanger voor pip/venv geschreven in Rust."
REQUIRED_SAFETY = SafetyLevel.SAFE

def apply_fix() -> bool:
    if shutil.which("uv"):
        print("\n✓ 'uv' is al geïnstalleerd!")
        return True

    print("\n--- 'uv' Installeren ---")
    print("uv zorgt voor razendsnelle pip-installs en venvs.")
    print("Aanbevolen officiële installatie: curl -LsSf https://astral.sh/uv/install.sh | sh\n")

    choice = input("'uv' nu installeren via de officiële installer? [y/N]: ").strip().lower()
    if choice == 'y':
        try:
            # Installeren via het officiële script
            subprocess.run("curl -LsSf https://astral.sh/uv/install.sh | sh", shell=True, check=True)
            print("\n✓ 'uv' is succesvol geïnstalleerd!")
            print("💡 Tip: Herstart je terminal of voer 'source ~/.cargo/env' uit om 'uv' direct te gebruiken.")
            return True
        except Exception as e:
            print(f"\n✗ Fout bij installeren via curl: {e}")
            print("Probeer het eventueel handmatig via: pip install uv")
            return False
    return False