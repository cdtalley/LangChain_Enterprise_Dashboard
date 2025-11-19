"""
Setup script that enforces Python 3.11 or 3.12
===============================================
This script will find and use Python 3.11 or 3.12 to create the virtual environment.
"""

import sys
import subprocess
import os
import shutil
import logging
from pathlib import Path
from typing import Optional, Tuple, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def find_python_311_or_312() -> Optional[Tuple[str, str]]:
    """
    Find Python 3.11 or 3.12 executable on the system.
    
    Returns:
        Tuple of (version, executable_path) if found, None otherwise
    """
    candidates: List[Tuple[str, str]] = []
    
    # Windows: Check py launcher
    if sys.platform == "win32":
        for version in ["3.12", "3.11"]:
            try:
                result = subprocess.run(
                    ["py", f"-{version}", "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    check=False
                )
                if result.returncode == 0:
                    # Get full path
                    result2 = subprocess.run(
                        ["py", f"-{version}", "-c", "import sys; print(sys.executable)"],
                        capture_output=True,
                        text=True,
                        timeout=5,
                        check=False
                    )
                    if result2.returncode == 0:
                        exe = result2.stdout.strip()
                        if exe and Path(exe).exists():
                            candidates.append((version, exe))
                            logger.debug(f"Found Python {version} via py launcher: {exe}")
            except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as e:
                logger.debug(f"Could not check Python {version} via py launcher: {e}")
                continue
    
    # Check common installation paths
    common_paths: List[str] = []
    if sys.platform == "win32":
        username = os.getenv("USERNAME", "")
        common_paths = [
            r"C:\Python312\python.exe",
            r"C:\Python311\python.exe",
            r"C:\Program Files\Python312\python.exe",
            r"C:\Program Files\Python311\python.exe",
            rf"C:\Users\{username}\AppData\Local\Programs\Python\Python312\python.exe",
            rf"C:\Users\{username}\AppData\Local\Programs\Python\Python311\python.exe",
        ]
    else:
        common_paths = [
            "/usr/bin/python3.12",
            "/usr/bin/python3.11",
            "/usr/local/bin/python3.12",
            "/usr/local/bin/python3.11",
            "/opt/homebrew/bin/python3.12",
            "/opt/homebrew/bin/python3.11",
        ]
    
    for path_str in common_paths:
        path = Path(path_str)
        if path.exists():
            try:
                result = subprocess.run(
                    [str(path), "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    check=False
                )
                if result.returncode == 0:
                    version_str = result.stdout.strip()
                    if "3.12" in version_str:
                        candidates.append(("3.12", str(path)))
                        logger.debug(f"Found Python 3.12 at: {path}")
                    elif "3.11" in version_str:
                        candidates.append(("3.11", str(path)))
                        logger.debug(f"Found Python 3.11 at: {path}")
            except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as e:
                logger.debug(f"Could not verify Python at {path}: {e}")
                continue
    
    # Prefer 3.12, then 3.11
    if candidates:
        candidates.sort(key=lambda x: x[0], reverse=True)
        logger.info(f"Found {len(candidates)} Python installation(s)")
        return candidates[0]
    
    logger.warning("No compatible Python version found")
    return None


def verify_python_version(python_exe: str) -> bool:
    """
    Verify that the Python executable is version 3.11 or 3.12.
    
    Args:
        python_exe: Path to Python executable
        
    Returns:
        True if version is valid, False otherwise
    """
    try:
        result = subprocess.run(
            [python_exe, "-c", "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False
        )
        if result.returncode == 0:
            version_str = result.stdout.strip()
            try:
                major, minor = map(int, version_str.split('.'))
                return major == 3 and minor in (11, 12)
            except ValueError:
                return False
        return False
    except Exception as e:
        logger.error(f"Failed to verify Python version: {e}")
        return False


def create_virtual_environment(python_exe: str, venv_path: Path) -> bool:
    """
    Create virtual environment using specified Python executable.
    
    Args:
        python_exe: Path to Python executable
        venv_path: Path where venv should be created
        
    Returns:
        True if successful, False otherwise
    """
    if venv_path.exists():
        logger.info(f"Removing existing virtual environment at {venv_path}")
        try:
            shutil.rmtree(venv_path)
        except OSError as e:
            logger.error(f"Failed to remove existing venv: {e}")
            return False
    
    try:
        logger.info(f"Creating virtual environment with {python_exe}")
        result = subprocess.run(
            [python_exe, "-m", "venv", str(venv_path)],
            check=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        logger.info("Virtual environment created successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to create venv: {e}")
        if e.stderr:
            logger.error(f"Error output: {e.stderr}")
        return False
    except subprocess.TimeoutExpired:
        logger.error("Virtual environment creation timed out")
        return False


def install_dependencies(pip_exe: Path) -> bool:
    """
    Install project dependencies using pip.
    
    Args:
        pip_exe: Path to pip executable
        
    Returns:
        True if successful, False otherwise
    """
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        logger.error("requirements.txt not found")
        return False
    
    # Upgrade pip first
    logger.info("Upgrading pip...")
    try:
        subprocess.run(
            [str(pip_exe), "install", "--upgrade", "pip"],
            check=True,
            timeout=300,
            capture_output=True
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        logger.warning(f"Failed to upgrade pip (non-critical): {e}")
    
    # Install requirements
    logger.info("Installing dependencies (this may take several minutes)...")
    try:
        result = subprocess.run(
            [str(pip_exe), "install", "-r", "requirements.txt"],
            check=True,
            timeout=1800,  # 30 minutes max
            capture_output=True,
            text=True
        )
        logger.info("Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install dependencies: {e}")
        if e.stderr:
            logger.error(f"Error output: {e.stderr[:500]}")  # Limit output
        return False
    except subprocess.TimeoutExpired:
        logger.error("Dependency installation timed out")
        return False


def main() -> None:
    """Main setup function"""
    print("=" * 70)
    print("Enterprise LangChain AI Workbench - Python Version Setup")
    print("=" * 70)
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
            print("=" * 70)
            print("ERROR: Python 3.11 or 3.12 not found!")
            print("=" * 70)
            print()
            print("Please install Python 3.12:")
            print("  Windows: https://www.python.org/downloads/release/python-3120/")
            print("  macOS:   brew install python@3.12")
            print("  Linux:   sudo apt install python3.12 python3.12-venv")
            print()
            print("After installing, run this script again.")
            sys.exit(1)
        
        version, python_exe = python_info
        
        # Verify the found Python version
        if not verify_python_version(python_exe):
            print(f"ERROR: Found Python at {python_exe} but version verification failed")
            sys.exit(1)
        
        print(f"Found Python {version} at: {python_exe}")
        print()
        print(f"Creating virtual environment with Python {version}...")
        
        venv_path = Path("venv")
        if not create_virtual_environment(python_exe, venv_path):
            print("ERROR: Failed to create virtual environment")
            sys.exit(1)
        
        # Get pip executable
        if sys.platform == "win32":
            pip_exe = venv_path / "Scripts" / "pip.exe"
        else:
            pip_exe = venv_path / "bin" / "pip"
        
        if not pip_exe.exists():
            print(f"ERROR: pip executable not found at {pip_exe}")
            sys.exit(1)
        
        # Install dependencies
        if not install_dependencies(pip_exe):
            print("ERROR: Failed to install dependencies")
            sys.exit(1)
        
        print()
        print("=" * 70)
        print("Setup Complete!")
        print("=" * 70)
        print()
        print("To activate the virtual environment:")
        if sys.platform == "win32":
            print("  venv\\Scripts\\activate")
            print("  Or: venv\\Scripts\\Activate.ps1")
        else:
            print("  source venv/bin/activate")
        print()
        print("Then run: python start_app.py")
        print("=" * 70)
    elif sys.version_info.minor < 11:
        print("ERROR: Python 3.11 or higher is required")
        print(f"   Current version: {current_version}")
        sys.exit(1)
    else:
        print("Python version OK - proceeding with setup...")
        # Run normal setup if available
        try:
            import setup
            setup.main()
        except ImportError:
            logger.warning("setup.py not found, skipping normal setup")
            print("Note: setup.py not found. Using current Python environment.")

if __name__ == "__main__":
    main()

