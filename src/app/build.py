import os
import subprocess
import sys

def resource_path(relative_path):
    import sys
    import os
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def main():
    print("=== Build exe pro project_builder ===")
    project_name = input("Název projektu (default: MyProject): ").strip() or "MyProject"
    version = input("Verze (default: 1.0.0): ").strip() or "1.0.0"
    author = input("Autor (default: Unknown): ").strip() or "Unknown"

    # cesta ke skriptu main.py a sablonam
    main_script = os.path.join("src", "app", "main.py")
    templates_folder = os.path.join("src", "templates")

    if not os.path.exists(main_script):
        print(f"Chyba: Nenalezen soubor {main_script}")
        sys.exit(1)
    if not os.path.exists(templates_folder):
        print(f"Chyba: Nenalezena složka {templates_folder}")
        sys.exit(1)

    dist_folder = "dist"
    build_folder = "build"

    # PyInstaller parametr --add-data, pozor na platformu
    if os.name == "nt":
        add_data = f"{templates_folder};templates"
    else:
        add_data = f"{templates_folder}:templates"

    # Připravíme příkaz pro PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",
        f"--name={project_name}",
        f"--add-data={add_data}",
        main_script,
    ]

    print("\nSpouštím PyInstaller...")
    print(" ".join(cmd))

    # Spustíme příkaz
    result = subprocess.run(cmd)

    if result.returncode != 0:
        print("Build se nezdařil.")
        sys.exit(1)

    print(f"\nBuild úspěšný! Výstup najdeš ve složce '{dist_folder}' pod názvem '{project_name}.exe'")

if __name__ == "__main__":
    main()
