# Quick Setup Guide

## 🚀 Automated Setup (Easiest)

### Windows
```bash
# Just run this:
setup.bat
```

### macOS/Linux
```bash
# Make executable (first time only)
chmod +x setup.sh

# Run setup
./setup.sh
```

### All Platforms (Python script)
```bash
python setup.py
```

The setup script will:
- ✅ Check Python version (requires 3.11 or 3.12)
- ✅ Create virtual environment
- ✅ Upgrade pip
- ✅ Install all dependencies
- ✅ Show you how to activate and run

## 📋 Manual Setup

### 1. Check Python Version
```bash
python --version
# Should be 3.11.x or 3.12.x
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment
```bash
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Run the App
```bash
streamlit run streamlit_app.py
```

## ⚠️ Python Version Requirements

- **Required**: Python 3.11 or 3.12
- **NOT Supported**: Python 3.13 (typing compatibility issues)

If you have Python 3.13, install Python 3.12:
- **Windows**: Download from https://www.python.org/downloads/
- **macOS**: `brew install python@3.12`
- **Linux**: `sudo apt install python3.12`

## ✅ Verification

After setup, verify everything works:
```bash
# Activate venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux

# Test imports
python -c "from agents import MultiAgentSystem; print('✅ Success')"

# Run app
streamlit run streamlit_app.py
```

