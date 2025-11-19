# Build Status & Verification

## ✅ Build Verification Script

Run this to verify your build:

```bash
python verify_build.py
```

This will check:
- Python version compatibility
- Core dependencies (Streamlit, Pandas, NumPy, LangChain, etc.)
- Optional dependencies (PyTorch, Transformers, etc.)
- Project modules (agents, advanced_rag, etc.)

## 🔧 Setup Scripts

### Quick Setup
```bash
# Windows
setup.bat

# macOS/Linux
chmod +x setup.sh
./setup.sh

# All platforms
python setup.py
```

## 📋 Requirements

### Python Version
- **Required**: Python 3.11 or 3.12
- **NOT Supported**: Python 3.13 (typing compatibility issues)

### Core Dependencies
All listed in `requirements.txt`:
- Streamlit (UI framework)
- LangChain (LLM orchestration)
- FastAPI (API framework)
- Pydantic (data validation)
- SQLAlchemy (database ORM)
- Pandas, NumPy (data processing)
- Plotly (visualizations)

### Optional Dependencies
- PyTorch (for fine-tuning)
- Transformers (HuggingFace models)
- PEFT (LoRA/QLoRA fine-tuning)
- Datasets (HuggingFace datasets)

## ✅ Verification Checklist

After setup, verify:

1. **Python Version**
   ```bash
   python --version  # Should be 3.11.x or 3.12.x
   ```

2. **Virtual Environment**
   ```bash
   # Check if activated (should see (venv) in prompt)
   # Windows: venv\Scripts\activate
   # macOS/Linux: source venv/bin/activate
   ```

3. **Core Imports**
   ```bash
   python -c "import streamlit; import pandas; import langchain; print('OK')"
   ```

4. **Project Modules**
   ```bash
   python -c "from agents import MultiAgentSystem; print('OK')"
   ```

5. **Run Verification Script**
   ```bash
   python verify_build.py
   ```

6. **Start Application**
   ```bash
   streamlit run streamlit_app.py
   ```

## 🐛 Common Issues

### Import Errors
- **Solution**: Activate venv and run `pip install -r requirements.txt`

### Python 3.13 Errors
- **Solution**: Install Python 3.12 and recreate venv

### Missing Dependencies
- **Solution**: Run `python setup.py` or `pip install -r requirements.txt`

### Virtual Environment Not Activated
- **Solution**: Activate venv before running scripts

## 📊 Build Status

Run `python verify_build.py` to get current build status.

