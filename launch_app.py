"""
Launch script that ensures correct Python version and virtual environment
=========================================================================
This script will:
1. Check Python version (must be 3.11 or 3.12)
2. Activate virtual environment if needed
3. Launch the Streamlit app
"""

import sys
import subprocess
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.11 or 3.12"""
    version = sys.version_info
    if version.major != 3:
        return False, f"Python 3 required, found {version.major}"
    if version.minor < 11:
        return False, f"Python 3.11+ required, found {version.major}.{version.minor}"
    if version.minor >= 13:
        return False, f"Python 3.13 NOT supported. Use Python 3.11 or 3.12"
    return True, f"Python {version.major}.{version.minor}.{version.micro}"

def get_venv_python():
    """Get Python executable from venv"""
    venv_path = Path("venv")
    if sys.platform == "win32":
        python_exe = venv_path / "Scripts" / "python.exe"
    else:
        python_exe = venv_path / "bin" / "python"
    
    if python_exe.exists():
        return python_exe
    return None

def main():
    """Launch the application"""
    print("="*70)
    print("Enterprise LangChain AI Workbench - Launcher")
    print("="*70)
    print()
    
    # Check if venv exists
    venv_python = get_venv_python()
    if not venv_python:
        print("ERROR: Virtual environment not found!")
        print()
        print("Please run setup first:")
        print("  python setup_correct_python.py")
        sys.exit(1)
    
    # Check venv Python version
    print("Checking virtual environment Python version...")
    try:
        result = subprocess.run(
            [str(venv_python), "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        print(f"  {result.stdout.strip()}")
        
        # Verify it's 3.11 or 3.12
        result2 = subprocess.run(
            [str(venv_python), "-c", "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"],
            capture_output=True,
            text=True,
            timeout=5
        )
        venv_version = result2.stdout.strip()
        minor = int(venv_version.split('.')[1])
        
        if minor >= 13:
            print()
            print("ERROR: Virtual environment uses Python 3.13 (incompatible)!")
            print("Please recreate venv with Python 3.11 or 3.12:")
            print("  python setup_correct_python.py")
            sys.exit(1)
        
        if minor < 11:
            print()
            print("ERROR: Virtual environment uses Python < 3.11!")
            print("Please recreate venv with Python 3.11 or 3.12:")
            print("  python setup_correct_python.py")
            sys.exit(1)
        
        print("  Version OK!")
    except Exception as e:
        print(f"  Warning: Could not verify version: {e}")
    
    print()
    print("Starting Streamlit application...")
    print("="*70)
    print()
    
    # Launch Streamlit using venv Python
    try:
        subprocess.run([
            str(venv_python), "-m", "streamlit", "run", "streamlit_app.py",
            "--server.headless", "false",
            "--server.port", "8501",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n\nApplication stopped by user")
    except Exception as e:
        print(f"\nERROR: Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

