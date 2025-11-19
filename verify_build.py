"""
Build Verification Script
=========================
Verifies that all critical imports work and the project is ready to run.
"""

import sys
import importlib

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major != 3:
        print("ERROR: Python 3 is required")
        return False
    if version.minor < 11:
        print("ERROR: Python 3.11+ is required")
        return False
    if version.minor >= 13:
        print("WARNING: Python 3.13 may have compatibility issues")
        print("   Recommended: Use Python 3.12")
    
    print("Python version OK")
    return True

def check_import(module_name, package_name=None, optional=False):
    """Check if a module can be imported"""
    try:
        importlib.import_module(module_name)
        print(f"OK: {package_name or module_name}")
        return True
    except ImportError as e:
        if optional:
            print(f"WARN: {package_name or module_name} (optional) - {str(e)[:50]}")
            return True
        else:
            print(f"FAIL: {package_name or module_name} - {str(e)[:50]}")
            return False
    except Exception as e:
        print(f"FAIL: {package_name or module_name} - {str(e)[:50]}")
        return False

def main():
    """Run build verification"""
    print("=" * 60)
    print("Build Verification")
    print("=" * 60)
    print()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    print("\nChecking Core Dependencies:")
    print("-" * 60)
    
    core_modules = [
        ("streamlit", "Streamlit"),
        ("pandas", "Pandas"),
        ("numpy", "NumPy"),
        ("plotly", "Plotly"),
        ("langchain", "LangChain"),
        ("langchain_community", "LangChain Community"),
        ("fastapi", "FastAPI"),
        ("pydantic", "Pydantic"),
        ("sqlalchemy", "SQLAlchemy"),
    ]
    
    core_ok = True
    for module, name in core_modules:
        if not check_import(module, name):
            core_ok = False
    
    print("\nChecking Optional Dependencies:")
    print("-" * 60)
    
    optional_modules = [
        ("torch", "PyTorch"),
        ("transformers", "Transformers"),
        ("peft", "PEFT"),
        ("datasets", "HuggingFace Datasets"),
        ("redis", "Redis"),
    ]
    
    for module, name in optional_modules:
        check_import(module, name, optional=True)
    
    print("\nChecking Project Modules:")
    print("-" * 60)
    
    project_modules = [
        ("agents", "agents.py"),
        ("advanced_rag", "advanced_rag.py"),
        ("model_registry", "model_registry.py"),
        ("ab_testing", "ab_testing.py"),
        ("experiment_tracking", "experiment_tracking.py"),
        ("model_monitoring", "model_monitoring.py"),
        ("llm_fine_tuning", "llm_fine_tuning.py"),
    ]
    
    project_ok = True
    for module, name in project_modules:
        if not check_import(module, name):
            project_ok = False
    
    print("\n" + "=" * 60)
    
    if core_ok and project_ok:
        print("BUILD VERIFICATION PASSED")
        print("=" * 60)
        print("\nYou can now run:")
        print("   streamlit run streamlit_app.py")
        print("   or")
        print("   python start_app.py")
        return 0
    else:
        print("BUILD VERIFICATION FAILED")
        print("=" * 60)
        print("\nSolution:")
        print("   1. Activate virtual environment")
        print("   2. Run: pip install -r requirements.txt")
        print("   3. Run this script again")
        return 1

if __name__ == "__main__":
    sys.exit(main())

