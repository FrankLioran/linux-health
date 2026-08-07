#!/usr/bin/env python3
import platform
import sys
from base import CheckCategory, Status
from config import SafetyLevel
from dev_stack import check_dev_stack
from generator import generate_html_report
from memory import check_memory

# Alle tune-modules importeren
import tune_swap
import tune_zram
import tune_cleanup
import tune_uv

# Lijst van alle beschikbare optimalisatiemodules
tune_modules = [
    tune_swap,
    tune_zram,
    tune_cleanup,
    tune_uv
]

# Kleurcodes voor de terminal
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"


def render_status(status: Status) -> str:
    if status == Status.OK:
        return f"{GREEN}{status.value}{RESET}"
    elif status == Status.WARN:
        return f"{YELLOW}{status.value}{RESET}"
    return f"{RED}{status.value}{RESET}"


def print_header():
    print("=" * 52)
    print("         Linux Health Manager 1.0")
    print("=" * 52)
    print(f"\nSysteem:\n {platform.system()} {platform.release()}")
    print(f" Architectuur: {platform.machine()}")
    print("-" * 40)


def main():
    print_header()

    categories: list[CheckCategory] = []
    total_deduction = 0

    # 1. Memory Checks
    mem_cat, mem_deduct = check_memory()
    categories.append(mem_cat)
    total_deduction += mem_deduct

    # 2. Dev & AI Stack Checks
    dev_cat, dev_deduct = check_dev_stack()
    categories.append(dev_cat)
    total_deduction += dev_deduct

    # Resultaten per categorie tonen
    for cat in categories:
        print(f"\n{cat.name}\n")
        for item in cat.items:
            print(f"{render_status(item.status)} {item.message}")
        print("-" * 40)

    # Health Score berekenen
    health_score = max(0, 100 - total_deduction)
    print(
        f"\nHealth Score\n\n{GREEN if health_score >= 80 else YELLOW}{health_score} / 100{RESET}\n"
    )

    # HTML Rapport genereren
    report_path = generate_html_report(categories, health_score)
    print(f"📄 Rapport opgeslagen in: {report_path}\n")

    # Interactive Fix Menu
    print("\nBeschikbare verbeteringen:\n")
    for idx, module in enumerate(tune_modules, 1):
        title = getattr(module, "TITLE", module.__name__)
        safety = getattr(module, "REQUIRED_SAFETY", SafetyLevel.SAFE)
        description = getattr(module, "DESCRIPTION", "Geen beschrijving beschikbaar.")

        print(f"  {idx}. {title} ({safety.name})")
        print(f"     └─ {description}\n")

    print("  0. Afsluiten\n")

    choice = input("Kies een optie: ").strip()

    # Dynamische verwerking van de keuze
    if choice.isdigit():
        idx = int(choice)
        if 1 <= idx <= len(tune_modules):
            selected_module = tune_modules[idx - 1]
            selected_module.apply_fix()
        elif idx == 0:
            print("Geen wijzigingen uitgevoerd. Fijne dag, Frank!")
        else:
            print("Ongeldige keuze. Geen wijzigingen uitgevoerd.")
    else:
        print("Geen geldige invoer. Fijne dag, Frank!")


if __name__ == "__main__":
    main()