import importlib
import subprocess
import sys
import re

def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except subprocess.CalledProcessError as e:
        print(f"Failed To Install {package}: {e}")

def is_package_installed(package):
    try:
        importlib.import_module(package)
        return True
    except ImportError:
        return False

def extract_packages(file_path):
    packages = set()
    with open(file_path, "r") as file:
        for line in file:
            match = re.match(r"^\s*(?:import|from)\s+([a-zA-Z0-9_]+)", line)
            if match:
                package = match.group(1).split('.')[0]
                packages.add(package)
    return packages

def main(file_path):
    print(f"Looking For Required Packages In {file_path}...")
    required_packages = extract_packages(file_path)

    for package in required_packages:
        if not is_package_installed(package):
            print(f"Installing {package}...")
            install_package(package)
        else:
            print(f"{package} Is Already Installed.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: Python Install_Requirements.py <python_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)
