# Installation Guide

## 🚀 Quick Start

### Windows
```bash
setup.bat
```

### macOS/Linux
```bash
chmod +x setup.sh
./setup.sh
```

### All Platforms
```bash
python setup.py
```

## 📋 Prerequisites

- **Python 3.11 or 3.12** (Python 3.13 NOT supported)
- **pip** (comes with Python)
- **git** (optional, for cloning)

## 🔧 Step-by-Step Installation

### 1. Verify Python Installation

```bash
python --version
# Should show: Python 3.11.x or Python 3.12.x
```

If you don't have Python or have Python 3.13:
- **Windows**: Download from https://www.python.org/downloads/
- **macOS**: `brew install python@3.12`
- **Linux**: `sudo apt install python3.12`

### 2. Run Setup Script

The setup script will automatically:
- ✅ Check Python version
- ✅ Create virtual environment (`venv/`)
- ✅ Upgrade pip to latest version
- ✅ Install all dependencies from `requirements.txt`

**Windows:**
```bash
setup.bat
```

**macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

**Or use Python:**
```bash
python setup.py
```

### 3. Activate Virtual Environment

After setup, activate the virtual environment:

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### 4. Verify Installation

```bash
# Test imports
python -c "from agents import MultiAgentSystem; print('✅ Success')"

# Check Streamlit
streamlit --version
```

### 5. Run the Application

```bash
# Option 1: Use start script
python start_app.py

# Option 2: Direct Streamlit
streamlit run streamlit_app.py
```

The app will open at: http://localhost:8501

## 🔄 Updating Dependencies

If you need to update dependencies:

```bash
# Activate venv first
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Upgrade pip
pip install --upgrade pip

# Update requirements
pip install --upgrade -r requirements.txt
```

## 🐛 Troubleshooting

### "Python not found"
- Make sure Python is installed and in PATH
- Windows: Check "Add Python to PATH" during installation
- Try `python3` instead of `python`

### "pip not found"
- Python should include pip
- Try `python -m pip` instead of `pip`

### "Virtual environment creation failed"
- Make sure you have write permissions in the directory
- Try running as administrator (Windows) or with sudo (Linux)

### "Import errors after installation"
- Make sure virtual environment is activated
- Check that dependencies installed: `pip list`
- Reinstall: `pip install -r requirements.txt --force-reinstall`

### "Streamlit not found"
- Activate virtual environment
- Install: `pip install streamlit`
- Or re-run setup script

## 📝 Notes

- The virtual environment (`venv/`) is excluded from git (see `.gitignore`)
- Each developer should create their own virtual environment
- Never commit the `venv/` directory
- Always activate venv before running the application

## ✅ Verification Checklist

- [ ] Python 3.11 or 3.12 installed
- [ ] Virtual environment created (`venv/` directory exists)
- [ ] Virtual environment activated (see `(venv)` in prompt)
- [ ] Dependencies installed (`pip list` shows packages)
- [ ] Imports work (`python -c "from agents import MultiAgentSystem"`)
- [ ] Streamlit runs (`streamlit run streamlit_app.py`)

## 🎯 Next Steps

After installation:
1. Read [README.md](README.md) for project overview
2. Check [QUICK_FIX.md](QUICK_FIX.md) for common issues
3. Explore the Streamlit dashboard
4. Review [PYTHON313_COMPATIBILITY.md](PYTHON313_COMPATIBILITY.md) if needed

