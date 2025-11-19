"""
Setup script that enforces Python 3.11 or 3.12
===============================================
This script will find and use Python 3.11 or 3.12 to create the virtual environment.
"""

import sys
import subprocess
import os
from pathlib import Path

def find_python_311_or_312():
    """Find Python 3.11 or 3.12 executable"""
    candidates = []
    
    # Windows: Check py launcher
    if sys.platform == "win32":
        for version in ["3.12", "3.11"]:
            try:
                result = subprocess.run(
                    ["py", f"-{version}", "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    # Get full path
                    result2 = subprocess.run(
                        ["py", f"-{version}", "-c", "import sys; print(sys.executable)"],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if result2.returncode == 0:
                        exe = result2.stdout.strip()
                        candidates.append((version, exe))
            except:
                pass
    
    # Check common paths
    common_paths = []
    if sys.platform == "win32":
        common_paths = [
            r"C:\Python312\python.exe",
            r"C:\Python311\python.exe",
            r"C:\Program Files\Python312\python.exe",
            r"C:\Program Files\Python311\python.exe",
            r"C:\Users\{}\AppData\Local\Programs\Python\Python312\python.exe".format(os.getenv("USERNAME", "")),
            r"C:\Users\{}\AppData\Local\Programs\Python\Python311\python.exe".format(os.getenv("USERNAME", "")),
        ]
    else:
        common_paths = [
            "/usr/bin/python3.12",
            "/usr/bin/python3.11",
            "/usr/local/bin/python3.12",
            "/usr/local/bin/python3.11",
        ]
    
    for path in common_paths:
        if Path(path).exists():
            try:
                result = subprocess.run(
                    [path, "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    version_str = result.stdout.strip()
                    if "3.12" in version_str:
                        candidates.append(("3.12", path))
                    elif "3.11" in version_str:
                        candidates.append(("3.11", path))
            except:
                pass
    
    # Prefer 3.12, then 3.11
    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0] if candidates else None

def main():
    """Main setup function"""
    print("="*70)
    print("Enterprise LangChain AI Workbench - Python Version Setup")
    print("="*70)
    print()
    
    # Check current Python version
    current_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"Current Python: {current_version}")
    
    if sys.version_info.minor >= 13:
        print("ERROR: Python 3.13 is NOT compatible with LangChain/Pydantic")
        print("       You MUST use Python 3.11 or 3.12")
        print()
        print("Searching for Python 3.11 or 3.12...")
        
        python_info = find_python_311_or_312()
        if not python_info:
            print()
            print("="*70)
            print("ERROR: Python 3.11 or 3.12 not found!")
            print("="*70)
            print()
            print("Please install Python 3.12:")
            print("  Windows: https://www.python.org/downloads/release/python-3120/")
            print("  macOS:   brew install python@3.12")
            print("  Linux:   sudo apt install python3.12 python3.12-venv")
            print()
            print("After installing, run this script again.")
            sys.exit(1)
        
        version, python_exe = python_info
        print(f"Found Python {version} at: {python_exe}")
        print()
        print("Creating virtual environment with Python {}...".format(version))
        
        venv_path = Path("venv")
        if venv_path.exists():
            print("Removing existing venv...")
            import shutil
            shutil.rmtree(venv_path)
        
        # Create venv with correct Python
        try:
            subprocess.run([python_exe, "-m", "venv", str(venv_path)], check=True)
            print("Virtual environment created!")
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Failed to create venv: {e}")
            sys.exit(1)
        
        # Get pip executable
        if sys.platform == "win32":
            pip_exe = venv_path / "Scripts" / "pip.exe"
        else:
            pip_exe = venv_path / "bin" / "pip"
        
        # Upgrade pip
        print("Upgrading pip...")
        try:
            subprocess.run([str(pip_exe), "install", "--upgrade", "pip"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"WARNING: Failed to upgrade pip: {e}")
        
        # Install requirements
        print("Installing dependencies (this may take several minutes)...")
        try:
            subprocess.run([str(pip_exe), "install", "-r", "requirements.txt"], check=True)
            print("Dependencies installed!")
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Failed to install dependencies: {e}")
            sys.exit(1)
        
        print()
        print("="*70)
        print("Setup Complete!")
        print("="*70)
        print()
        print("To activate the virtual environment:")
        if sys.platform == "win32":
            print("  venv\\Scripts\\activate")
            print("  Or: venv\\Scripts\\Activate.ps1")
        else:
            print("  source venv/bin/activate")
        print()
        print("Then run: python start_app.py")
        print("="*70)
    else:
        print("Python version OK - proceeding with setup...")
        # Run normal setup
        import setup
        setup.main()

if __name__ == "__main__":
    main()

