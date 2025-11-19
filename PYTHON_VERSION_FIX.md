# Python Version Fix - CRITICAL

## Problem
The app was running with Python 3.13 (system Python) instead of Python 3.12 (venv).

## Solution
Always use the venv Python executable to run the app:

```bash
# Windows
venv\Scripts\python.exe -m streamlit run streamlit_app.py

# Or use the launcher
venv\Scripts\python.exe launch_app.py
```

## Why This Matters
- Python 3.13 has breaking changes with LangChain/Pydantic
- Python 3.12 is fully compatible
- The venv was created with Python 3.12

## Verification
Check which Python is being used:
```bash
venv\Scripts\python.exe --version
# Should show: Python 3.12.x
```

## Fixed Files
- `launch_app.py`: Now enforces venv Python usage
- App will fail fast if wrong Python version detected

