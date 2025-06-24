import os
import subprocess
import sys

def main():
    print("=== Build exe pro project_builder ===")
    project_name = input("Název projektu (default: MyProject): ").strip() or "MyProject"
    version = input("Verze (default: 1.0.0): ").strip() or "1.0.0"
    author = input("Autor (default: Unknown): ").strip() or "Unknown"

    # Relativní a absolutní cesty
    main_script = os.path.join("app", "main.py")
    templates_folder = os.path.join("templates")
    main_script_abs = os.path.abspath(main_script)
    templates_folder_abs = os.path.abspath(templates_folder)

    print(f"\n[DEBUG] Absolutní cesta k main.py: {main_script_abs}")
    print(f"[DEBUG] Absolutní cesta k templates: {templates_folder_abs}")

    if not os.path.exists(main_script_abs):
        print(f"❌ Chyba: Nenalezen soubor {main_script_abs}")
        sys.exit(1)
    if not os.path.exists(templates_folder_abs):
        print(f"❌ Chyba: Nenalezena složka {templates_folder_abs}")
        sys.exit(1)

    print("\n[DEBUG] Obsah složky templates:")
    for root, dirs, files in os.walk(templates_folder_abs):
        for name in files:
            print(f"  - {os.path.join(root, name)}")

    # Platform-specific add-data syntax
    if os.name == "nt":
        add_data = f"{templates_folder_abs};templates"
    else:
        add_data = f"{templates_folder_abs}:templates"

    print(f"\n[DEBUG] --add-data parametr: {add_data}")

    # Výstupní složky
    dist_folder = os.path.abspath("dist")
    build_folder = os.path.abspath("build")

    # Vytvoření složek, pokud neexistují
    os.makedirs(dist_folder, exist_ok=True)
    os.makedirs(build_folder, exist_ok=True)

    # Sestavení příkazu
    cmd = [
        "pyinstaller",
        "--onefile",
        "--clean",
        f"--name={project_name}",
        f"--distpath={dist_folder}",
        f"--workpath={build_folder}",
        f"--add-data={add_data}",
        main_script_abs,
    ]

    print("\n▶️ Spouštím PyInstaller...")
    print(" ".join(cmd))

    result = subprocess.run(cmd)

    if result.returncode != 0:
        print("\n❌ Build se nezdařil.")
        sys.exit(1)

    print(f"\n✅ Build úspěšný! Výstup: {os.path.join(dist_folder, f'{project_name}.exe')}")

if __name__ == "__main__":
    main()
