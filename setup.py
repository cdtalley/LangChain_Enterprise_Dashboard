"""
Setup script for Enterprise LangChain AI Workbench
==================================================
Properly sets up the virtual environment and installs all dependencies.
"""

import sys
import subprocess
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major != 3:
        print("ERROR: Python 3 is required")
        return False
    if version.minor < 11:
        print("ERROR: Python 3.11 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    if version.minor >= 13:
        print("WARNING: Python 3.13 has compatibility issues")
        print("   Recommended: Use Python 3.12 for best compatibility")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        response = input("   Continue anyway? (y/n): ").lower()
        if response != 'y':
            return False
    print(f"Python version: {version.major}.{version.minor}.{version.micro} - OK")
    return True

def create_venv(venv_path="venv"):
    """Create virtual environment"""
    if venv_path.exists():
        print(f"Virtual environment already exists at {venv_path}")
        return True
    
    print(f"Creating virtual environment at {venv_path}...")
    try:
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
        print(f"Virtual environment created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to create virtual environment: {e}")
        return False

def get_pip_executable(venv_path="venv"):
    """Get pip executable path for the virtual environment"""
    if sys.platform == "win32":
        return venv_path / "Scripts" / "pip.exe"
    else:
        return venv_path / "bin" / "pip"

def get_python_executable(venv_path="venv"):
    """Get Python executable path for the virtual environment"""
    if sys.platform == "win32":
        return venv_path / "Scripts" / "python.exe"
    else:
        return venv_path / "bin" / "python"

def upgrade_pip(venv_path="venv"):
    """Upgrade pip in virtual environment"""
    pip_exe = get_pip_executable(venv_path)
    if not pip_exe.exists():
        print(f"ERROR: pip not found at {pip_exe}")
        return False
    
    print("Upgrading pip...")
    try:
        subprocess.run([str(pip_exe), "install", "--upgrade", "pip"], check=True)
        print("pip upgraded successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to upgrade pip: {e}")
        return False

def install_requirements(venv_path="venv"):
    """Install requirements from requirements.txt"""
    pip_exe = get_pip_executable(venv_path)
    requirements_file = Path("requirements.txt")
    
    if not requirements_file.exists():
        print("ERROR: requirements.txt not found")
        return False
    
    print("Installing dependencies from requirements.txt...")
    print("   This may take several minutes...")
    try:
        subprocess.run(
            [str(pip_exe), "install", "-r", str(requirements_file)],
            check=True
        )
        print("All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to install dependencies: {e}")
        return False

def print_activation_instructions(venv_path="venv"):
    """Print instructions for activating the virtual environment"""
    print("\n" + "="*60)
    print("Setup Complete!")
    print("="*60)
    print("\nTo activate the virtual environment:")
    
    if sys.platform == "win32":
        print(f"   {venv_path}\\Scripts\\activate")
        print("\n   Or in PowerShell:")
        print(f"   {venv_path}\\Scripts\\Activate.ps1")
    else:
        print(f"   source {venv_path}/bin/activate")
    
    print("\nTo run the Streamlit app:")
    print("   streamlit run streamlit_app.py")
    print("\nFor more information, see README.md")
    print("="*60)

def main():
    """Main setup function"""
    print("="*60)
    print("Enterprise LangChain AI Workbench - Setup")
    print("="*60)
    print()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Determine venv path
    venv_path = Path("venv")
    
    # Create virtual environment
    if not create_venv(venv_path):
        sys.exit(1)
    
    # Upgrade pip
    if not upgrade_pip(venv_path):
        sys.exit(1)
    
    # Install requirements
    if not install_requirements(venv_path):
        sys.exit(1)
    
    # Print instructions
    print_activation_instructions(venv_path)

if __name__ == "__main__":
    main()
