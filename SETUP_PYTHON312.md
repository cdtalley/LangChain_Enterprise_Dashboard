# Setting Up Python 3.12 Environment

## Quick Setup Guide

You already have Python 3.12.6 installed! Here's how to use it:

### Step 1: Create Virtual Environment (Already Done)
```bash
py -3.12 -m venv venv312
```

### Step 2: Activate Virtual Environment

**PowerShell:**
```powershell
venv312\Scripts\Activate.ps1
```

**Command Prompt (CMD):**
```cmd
venv312\Scripts\activate.bat
```

### Step 3: Install Dependencies (In Batches)

Due to memory constraints, install in smaller batches:

```bash
# Core dependencies
pip install sqlalchemy>=2.0.23 streamlit pandas numpy

# LangChain dependencies  
pip install langchain langchain-community langchain-openai langchain-chroma

# ML/Data Science
pip install scikit-learn scipy joblib plotly

# FastAPI
pip install fastapi uvicorn pydantic

# Optional: Install rest as needed
pip install -r requirements.txt
```

### Step 4: Test Import
```bash
python -c "from model_registry import ModelRegistryManager; print('✅ Success!')"
```

### Step 5: Run Streamlit App
```bash
streamlit run streamlit_app.py
```

## Alternative: Use Existing Python 3.12 Installation

If you prefer to use your system Python 3.12 directly:

```bash
# Use Python 3.12 launcher
py -3.12 -m pip install sqlalchemy>=2.0.23 streamlit pandas numpy
py -3.12 -m streamlit run streamlit_app.py
```

## Verify Python Version

```bash
venv312\Scripts\python.exe --version
# Should show: Python 3.12.6
```

## Troubleshooting

**If you get "Activate.ps1 cannot be loaded":**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**If installation runs out of memory:**
- Install packages in smaller batches
- Close other applications
- Restart terminal and try again


