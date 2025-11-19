# Quick Start Guide - IMPORTANT

## ⚠️ CRITICAL: Always Use Venv Python

**DO NOT** run the app with system Python (3.13). Always use the venv Python (3.12).

## Correct Way to Start the App

### Option 1: Use the Launcher (Recommended)
```bash
venv\Scripts\python.exe launch_app.py
```

### Option 2: Direct Streamlit Command
```bash
venv\Scripts\python.exe -m streamlit run streamlit_app.py --server.port 8501
```

### Option 3: Activate Venv First
```bash
# Windows PowerShell
venv\Scripts\Activate.ps1

# Then run
streamlit run streamlit_app.py
```

## ❌ WRONG Ways (Will Cause Python 3.13 Errors)

```bash
# DON'T DO THIS - Uses system Python 3.13
python streamlit_app.py
python -m streamlit run streamlit_app.py
streamlit run streamlit_app.py  # If venv not activated
```

## Verify You're Using Correct Python

Before running, check:
```bash
venv\Scripts\python.exe --version
# Should show: Python 3.12.x
```

## Troubleshooting

If you see `TypeError: <class 'langchain_core.runnables.base.RunnableSerializable'> is not a generic class`:

1. **Stop all Python processes**
2. **Use venv Python**: `venv\Scripts\python.exe launch_app.py`
3. **Verify**: Check that the Python path in the error message shows `venv\Scripts\python.exe`, not `Python313`

## Why This Matters

- Python 3.13 has breaking changes with LangChain/Pydantic
- Your venv was created with Python 3.12 (compatible)
- System Python 3.13 will cause import errors

## Quick Fix Script

Create `start.bat`:
```batch
@echo off
venv\Scripts\python.exe launch_app.py
```

Then just run: `start.bat`
