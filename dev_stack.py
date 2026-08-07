# dev_stack.py
import shutil
import subprocess
from base import CheckCategory, CheckItem, Status

def check_dev_stack() -> tuple[CheckCategory, int]:
    cat = CheckCategory(name="AI & Dev Stack")
    score_deduction = 0

    # 1. NVIDIA / CUDA Check
    if shutil.which("nvidia-smi"):
        try:
            output = subprocess.check_output(["nvidia-smi", "--query-gpu=gpu_name,driver_version", "--format=csv,noheader"], text=True).strip()
            cat.items.append(CheckItem("GPU", Status.OK, f"NVIDIA GPU actief ({output})"))
        except Exception:
            cat.items.append(CheckItem("GPU", Status.WARN, "NVIDIA driver aanwezig, maar nvidia-smi geeft geen respons"))
            score_deduction += 5
    else:
        cat.items.append(CheckItem("GPU", Status.WARN, "Geen NVIDIA driver/GPU gedetecteerd (nvidia-smi ontbreekt)"))

    # 2. Docker Check
    if shutil.which("docker"):
        try:
            res = subprocess.run(["systemctl", "is-active", "docker"], capture_output=True, text=True)
            if res.stdout.strip() == "active":
                cat.items.append(CheckItem("Docker", Status.OK, "Docker service is actief"))
            else:
                cat.items.append(CheckItem("Docker", Status.WARN, "Docker geïnstalleerd, maar service staat uit"))
        except Exception:
            cat.items.append(CheckItem("Docker", Status.OK, "Docker aanwezig"))
    else:
        cat.items.append(CheckItem("Docker", Status.WARN, "Docker niet geïnstalleerd"))

    # 3. Python Package Managers (uv / pip)
    has_uv = shutil.which("uv") is not None
    has_pip = shutil.which("pip") is not None or shutil.which("pip3") is not None

    if has_uv:
        cat.items.append(CheckItem("Python Tool", Status.OK, "Bliksemsnelle pakketbeheerder 'uv' aanwezig"))
    else:
        cat.items.append(CheckItem("Python Tool", Status.WARN, "'uv' niet gevonden (aanbevolen voor snelle venvs)"))

    # 4. Ollama Check
    if shutil.which("ollama"):
        cat.items.append(CheckItem("AI Local", Status.OK, "Ollama aanwezig voor lokale LLM's"))

    return cat, score_deduction