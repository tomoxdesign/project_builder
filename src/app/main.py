import os
import sys
import time
from datetime import datetime
from tkinter import filedialog, Tk

# ANSI escape sekvence pro barvy
RESET = "\033[0m"
BOLD = "\033[1m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RED = "\033[91m"

def prompt(label, default=""):
    user_input = input(f"{YELLOW}{label}{RESET} ")
    return user_input.strip() or default

def get_project_info():
    print("\n" + f"{BOLD}{BLUE}{'=' * 50}")
    print("📁 GENERÁTOR PROJEKTOVÉ STRUKTURY")
    print(f"{'=' * 50}{RESET}\n")

    print("Budu se tě postupně ptát na několik údajů potřebných pro vytvoření struktury projektu.\n")
    print("Pokud některý údaj nevyplníš (tj. pouze stiskneš Enter), bude automaticky doplněna výchozí hodnota, kterou můžeš později upravit přímo v souborech.\n")
    print("Položky označené symbolem [*] jsou povinné a je nutné je vyplnit, jinak nebude možné pokračovat.\n")

    project_name = prompt("[D] Název projektu:", "moje-aplikace")
    author = prompt("[D] Autor:", "Neznámý autor")
    description = prompt("[D] Popis programu:", "*Zde doplňte popis programu.*")
    technologies = prompt("[D] Použité technologie (oddělené čárkami):", "*Zde doplňte použité technologie.*")
    usage_description = prompt("[D] Instrukce ke spuštění programu:", "*Zde doplňte informace pro spuštění programu.*")
    install_description = prompt("[D] Instrukce k instalaci programu:", "*Zde doplňte informace pro instalaci programu.*")
    packages = prompt("[D] Balíčky potřebné pro requirements (oddělené čárkami):")
    list_of_packages = "\n".join([pkg.strip() for pkg in packages.split(",") if pkg.strip()])

    print(f"\n{YELLOW}[#] Vyber typ licence:{RESET}")
    print("  1. MIT\n  2. Apache-2.0\n  3. BSD-3-Clause\n  4. GPL-3.0")
    choice = input("Zadej číslo licence (1–4): ").strip()

    license_options = {
        "1": "MIT",
        "2": "Apache-2.0",
        "3": "BSD-3-Clause",
        "4": "GPL-3.0"
    }

    if choice not in license_options:
        print(f"{RED}❌ Neplatná volba licence. Ukončuji.{RESET}")
        sys.exit(1)

    license_type = license_options[choice]

    print(f"\n{BOLD}📂 Vyber složku, kde se vytvoří projektová složka:{RESET}\n")
    Tk().withdraw()
    base_dir = filedialog.askdirectory()
    if not base_dir:
        print(f"{RED}❌ Nebyla vybrána žádná složka. Ukončuji.{RESET}")
        sys.exit(1)

    target_dir = os.path.join(base_dir, project_name)
    os.makedirs(target_dir, exist_ok=True)

    print(f"\n{GREEN}✅ Projekt úspěšně vytvořen ve složce: {target_dir}{RESET}\n")

    date = datetime.now().strftime("%d.%m.%Y")
    year = datetime.now().strftime("%Y")

    return {
        "project_name": project_name,
        "author": author,
        "description": description,
        "technologies": technologies,
        "license_type": license_type,
        "date": date,
        "year": year,
        "target_dir": target_dir,
        "usage_description": usage_description,
        "install_description": install_description,
        "list_of_packages": list_of_packages
    }

# Nová funkce pro správné načtení cesty k datům i v exe
def resource_path(relative_path):
    """Získá absolutní cestu k resource, i když je program spuštěn jako PyInstaller exe."""
    try:
        base_path = sys._MEIPASS  # pokud běží jako exe, složka dočasného rozbalení
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# ==== funkce na nahrazeni promennych v sablonach ====
def replace_placeholders(content, context):
    for key, value in context.items():
        content = content.replace(f"${{{key}}}", value)
    return content

# ==== funkce pro zpracovani sablon ====
def process_templates(context):
    # Použij resource_path pro složku templates
    templates_path = resource_path(os.path.join("templates"))

    print(f"{BLUE}[DEBUG] Templates path: {templates_path}{RESET}")

    # Cesty ke složkám v cílovém projektu
    root_dst = context["target_dir"]
    docs_cs_dst = os.path.join(root_dst, "docs", "cs")
    docs_en_dst = os.path.join(root_dst, "docs", "en")
    os.makedirs(docs_cs_dst, exist_ok=True)
    os.makedirs(docs_en_dst, exist_ok=True)

    # 1. Zpracování docs/cs
    cs_tpl_path = os.path.join(templates_path, "docs", "cs")
    license_file_cs = f"LICENSE.{context['license_type']}.cs.tpl"
    readme_cs_file = "README.cs.tpl"

    files_cs = [(license_file_cs, "LICENSE"), (readme_cs_file, "README.md")]
    print(f"{BLUE}[DEBUG] Zpracovávám CS šablony v: {cs_tpl_path}{RESET}")

    for tpl_name, output_name in files_cs:
        tpl_path = os.path.join(cs_tpl_path, tpl_name)
        if not os.path.isfile(tpl_path):
            print(f"Chyba: Šablona {tpl_name} neexistuje. Hledáno v: {tpl_path}")
            sys.exit(1)
        with open(tpl_path, "r", encoding="utf-8") as f:
            content = f.read()
        result = replace_placeholders(content, context)
        with open(os.path.join(docs_cs_dst, output_name), "w", encoding="utf-8") as f:
            f.write(result)

    # 2. Zpracování docs/en
    en_tpl_path = os.path.join(templates_path, "docs", "en")
    license_file_en = f"LICENSE.{context['license_type']}.en.tpl"
    readme_en_file = "README.en.tpl"

    files_en = [(license_file_en, "LICENSE"), (readme_en_file, "README.md")]

    for tpl_name, output_name in files_en:
        tpl_path = os.path.join(en_tpl_path, tpl_name)
        if not os.path.isfile(tpl_path):
            print(f"Chyba: Šablona {tpl_name} neexistuje. Hledáno v: {tpl_path}")
            sys.exit(1)
        with open(tpl_path, "r", encoding="utf-8") as f:
            content = f.read()
        result = replace_placeholders(content, context)
        with open(os.path.join(docs_en_dst, output_name), "w", encoding="utf-8") as f:
            f.write(result)

    # 3. Zpracování root šablon
    root_tpl_path = os.path.join(templates_path, "root")
    for filename in os.listdir(root_tpl_path):
        src_file = os.path.join(root_tpl_path, filename)
        with open(src_file, "r", encoding="utf-8") as f:
            content = f.read()
        result = replace_placeholders(content, context)

        if filename.startswith("LICENSE"):
            target_filename = "LICENSE"
        elif filename.startswith("requirements"):
            target_filename = "requirements.txt"
        else:
            target_filename = filename.replace(".tpl", ".md")

        dst_file = os.path.join(root_dst, target_filename)
        with open(dst_file, "w", encoding="utf-8") as f:
            f.write(result)

# ==== hlavní spuštění ====
if __name__ == "__main__":
    context = get_project_info()
    process_templates(context)
    print(f"\n{GREEN}✅ Projekt úspěšně vytvořen ve složce: {context['target_dir']}{RESET}")
    time.sleep(30)
    input(f"\n{BLUE}Stiskni Enter pro ukončení...{RESET}")
