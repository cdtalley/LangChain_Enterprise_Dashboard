"""
Enhanced Boot Script for Enterprise LangChain AI Workbench
===========================================================
Professional startup with impressive visuals and smooth initialization.
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def print_banner():
    """Print impressive startup banner."""
    banner = """
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                                                                          ║
    ║     🚀 ENTERPRISE LANGCHAIN AI WORKBENCH 🚀                              ║
    ║                                                                          ║
    ║     Production-Ready Multi-Agent AI Platform                             ║
    ║     Advanced MLOps • Real-Time Analytics • Enterprise Architecture      ║
    ║                                                                          ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)
    print()

def check_requirements():
    """Check system requirements."""
    print("🔍 Checking System Requirements...")
    print("=" * 70)
    
    # Check Python version
    version = sys.version_info
    if version.major != 3 or version.minor < 11 or version.minor >= 13:
        print(f"❌ Python Version: {version.major}.{version.minor}.{version.micro}")
        print("   Required: Python 3.11 or 3.12")
        return False
    print(f"✅ Python Version: {version.major}.{version.minor}.{version.micro}")
    
    # Check virtual environment
    in_venv = (
        hasattr(sys, 'real_prefix') or
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    )
    if in_venv:
        print("✅ Virtual Environment: Active")
    else:
        print("⚠️  Virtual Environment: Not detected (recommended)")
    
    # Check key dependencies
    required_modules = ['streamlit', 'langchain', 'pandas', 'numpy']
    missing = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}: Installed")
        except ImportError:
            print(f"❌ {module}: Missing")
            missing.append(module)
    
    if missing:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    print("\n" + "=" * 70)
    print("✅ All Requirements Met!")
    print()
    return True

def print_features():
    """Print impressive feature list."""
    features = """
    ✨ Key Features:
    
    🤖 Multi-Agent System      → Specialized AI agents with intelligent routing
    📊 Advanced RAG            → Hybrid semantic + keyword search
    🎓 LLM Fine-Tuning         → LoRA, QLoRA, PEFT methods
    📦 Model Registry          → Versioning & lifecycle management
    🧪 A/B Testing             → Statistical significance testing
    📝 Experiment Tracking     → MLflow-like tracking system
    🔍 Model Monitoring         → Performance & drift detection
    📚 Datasets & Models       → Pre-loaded datasets with training
    🔧 Tool Execution          → Secure code execution sandbox
    📈 Analytics Dashboard     → Real-time metrics & insights
    
    """
    print(features)

def main():
    """Main boot function."""
    print_banner()
    
    if not check_requirements():
        print("\n❌ System check failed. Please fix the issues above.")
        sys.exit(1)
    
    print_features()
    
    print("🚀 Starting Application...")
    print("=" * 70)
    print()
    print("📊 Dashboard will open at: http://localhost:8501")
    print("🌐 API Server available at: http://localhost:8000")
    print()
    print("💡 Tips:")
    print("   • Start with the Welcome tab for an overview")
    print("   • Try the Multi-Agent System for AI collaboration")
    print("   • Explore Advanced RAG for document analysis")
    print("   • Check out Model Registry for MLOps features")
    print()
    print("⏹️  Press Ctrl+C to stop the application")
    print("=" * 70)
    print()
    
    # Small delay for dramatic effect
    time.sleep(1)
    
    # Get script directory
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    
    # Start Streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.headless", "false",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n\n" + "=" * 70)
        print("👋 Application stopped by user")
        print("=" * 70)
    except FileNotFoundError:
        print("\n❌ Error: streamlit not found")
        print("💡 Solution: pip install streamlit")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        print("💡 Check that all dependencies are installed")
        sys.exit(1)

if __name__ == "__main__":
    main()

