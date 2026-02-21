# Python Version Requirements & Setup

## ⚠️ Important: Use Python 3.12 (Recommended)

**This project requires Python 3.11 or 3.12. Python 3.13 is NOT supported** due to typing strictness issues with Pydantic, SQLAlchemy, and LangChain.

## 🔧 Installation

### Check Your Python Version

```bash
python --version
# Should show: Python 3.11.x or Python 3.12.x
```

### Install Python 3.12

**Windows:**
- Download from [python.org](https://www.python.org/downloads/)
- Select Python 3.12.x
- During installation, check "Add Python to PATH"
- Or use Python launcher: `py -3.12`

**macOS:**
```bash
brew install python@3.12
```

**Linux:**
```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-pip
```

### Create Virtual Environment with Python 3.12

**Windows:**
```bash
# Using Python launcher (recommended)
py -3.12 -m venv venv312

# Or direct Python
python3.12 -m venv venv312

# Activate (PowerShell)
venv312\Scripts\Activate.ps1

# Activate (CMD)
venv312\Scripts\activate.bat
```

**macOS/Linux:**
```bash
python3.12 -m venv venv312
source venv312/bin/activate
```

### Install Dependencies

For systems with memory constraints, install in batches:

```bash
# Core dependencies
pip install --upgrade pip
pip install sqlalchemy>=2.0.23 streamlit pandas numpy

# LangChain dependencies  
pip install langchain langchain-community langchain-openai langchain-chroma

# ML/Data Science
pip install scikit-learn scipy joblib plotly

# FastAPI
pip install fastapi uvicorn pydantic

# Or install all at once (if you have enough memory)
pip install -r requirements.txt
```

## ✅ Verification

```bash
# Verify Python version
python --version  # Should be 3.11.x or 3.12.x
# Or on Windows:
venv312\Scripts\python.exe --version

# Test imports
python -c "from agents import MultiAgentSystem; print('✅ Success')"

# Run Streamlit app
streamlit run streamlit_app.py
```

## 🚀 Quick Start

**Windows (using venv Python directly):**
```bash
venv312\Scripts\python.exe launch_app.py
```

**All platforms (with activated venv):**
```bash
# Activate venv first, then:
streamlit run streamlit_app.py
```

## 🐛 Troubleshooting

**PowerShell execution policy error:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Installation runs out of memory:**
- Install packages in smaller batches (see above)
- Close other applications
- Restart terminal and try again

**TypeError with LangChain:**
- Ensure you're using venv Python (3.12), not system Python (3.13)
- Verify: `python --version` should show 3.12.x
- Use: `venv312\Scripts\python.exe` on Windows

## 📝 Notes

- Python 3.13 has stricter typing that breaks compatibility with many libraries
- Python 3.12 is the recommended version for this project
- All dependencies are tested and work with Python 3.11 and 3.12
- Always use venv Python, not system Python
