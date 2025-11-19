"""
Quick Start Script for Enterprise LangChain AI Workbench
=========================================================
Starts the Streamlit application with proper configuration.
Checks for virtual environment and provides helpful error messages.
"""

import subprocess
import sys
import os
from pathlib import Path

def check_venv():
    """Check if we're in a virtual environment"""
    in_venv = (
        hasattr(sys, 'real_prefix') or
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    )
    
    venv_path = Path("venv")
    venv_exists = venv_path.exists()
    
    return in_venv, venv_exists

def check_python_version():
    """Check Python version compatibility"""
    version = sys.version_info
    if version.major != 3:
        return False, f"Python 3 required, found {version.major}"
    if version.minor < 11:
        return False, f"Python 3.11+ required, found {version.major}.{version.minor}"
    if version.minor >= 13:
        return False, f"Python 3.13 not supported. Please use Python 3.11 or 3.12"
    return True, f"Python {version.major}.{version.minor}.{version.micro}"

def main():
    """Start the Streamlit application"""
    print("🚀 Starting Enterprise LangChain AI Workbench...")
    print("=" * 60)
    
    # Check Python version
    version_ok, version_msg = check_python_version()
    if not version_ok:
        print(f"❌ {version_msg}")
        print("\n💡 Solution:")
        print("  1. Install Python 3.11 or 3.12")
        print("  2. Run: python setup.py")
        print("  3. Activate venv and try again")
        sys.exit(1)
    print(f"✅ {version_msg}")
    
    # Check virtual environment
    in_venv, venv_exists = check_venv()
    
    if not in_venv:
        print("⚠️  Warning: Not running in a virtual environment")
        if venv_exists:
            print("\n💡 Solution:")
            print("  Windows: venv\\Scripts\\activate")
            print("  macOS/Linux: source venv/bin/activate")
            print("  Then run this script again")
        else:
            print("\n💡 Solution:")
            print("  Run: python setup.py")
            print("  This will create venv and install dependencies")
        print("\n" + "=" * 60)
        response = input("Continue anyway? (y/n): ").lower()
        if response != 'y':
            sys.exit(0)
    else:
        print("✅ Running in virtual environment")
    
    print("\n📊 Streamlit Dashboard will open at: http://localhost:8501")
    print("🔧 API Server can be started separately with: uvicorn enterprise_features:app --reload")
    print("=" * 60)
    print("\n✨ Features available:")
    print("  - 🤖 Multi-Agent System")
    print("  - 📊 Advanced RAG")
    print("  - 🎓 LLM Fine-Tuning (LoRA/QLoRA)")
    print("  - 📦 Model Registry")
    print("  - 🧪 A/B Testing")
    print("  - 📝 Experiment Tracking")
    print("  - 🔍 Model Monitoring")
    print("  - 📚 Datasets & Models")
    print("\n" + "=" * 60)
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Start Streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.headless", "false",
            "--server.port", "8501"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped by user")
    except FileNotFoundError:
        print("\n❌ Error: streamlit not found")
        print("💡 Solution: Run 'python setup.py' to install dependencies")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        print("💡 Solution: Make sure virtual environment is activated and dependencies are installed")
        sys.exit(1)

if __name__ == "__main__":
    main()

