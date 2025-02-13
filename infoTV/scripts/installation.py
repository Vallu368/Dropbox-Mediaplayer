import subprocess
import sys

# Function to check and install missing packages
def install_missing_packages():
    required_packages = [
        'vlc', 'pygetwindow', 'pyautogui', 'Pillow', 'pypdfium2', 'dropbox'
    ]
    for package in required_packages:
        try:
            __import__(package)  # Try importing the package
            print(f"Package '{package}' is already installed.")
        except ImportError:
            print(f"Package '{package}' is missing. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"Package '{package}' has been installed.")

# Install missing packages
install_missing_packages()
