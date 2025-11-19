# Python Version Requirements

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

```bash
# Windows
python3.12 -m venv venv312
venv312\Scripts\activate

# macOS/Linux
python3.12 -m venv venv312
source venv312/bin/activate
```

### Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## ✅ Verification

```bash
# Verify Python version
python --version  # Should be 3.11.x or 3.12.x

# Test imports
python -c "from agents import MultiAgentSystem; print('✅ Success')"

# Run Streamlit app
streamlit run streamlit_app.py
```

## 📝 Notes

- Python 3.13 has stricter typing that breaks compatibility with many libraries
- Python 3.12 is the recommended version for this project
- All dependencies are tested and work with Python 3.11 and 3.12
