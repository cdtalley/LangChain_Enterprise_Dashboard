# 📚 Datasets Module

Production-ready dataset loaders and model training scripts for ML showcase.

## Available Datasets

### 1. **Wine Quality** 🍷
- **Type**: Classification
- **Samples**: ~1,600
- **Features**: 11 physicochemical properties
- **Task**: Predict wine quality (0-10 scale)
- **Source**: UCI ML Repository

### 2. **Breast Cancer Wisconsin** 🏥
- **Type**: Binary Classification
- **Samples**: ~570
- **Features**: 30 cell nucleus measurements
- **Task**: Diagnose breast cancer (malignant/benign)
- **Source**: sklearn

### 3. **Credit Card Fraud Detection** 💳
- **Type**: Binary Classification (Imbalanced)
- **Samples**: ~10,000
- **Features**: 7 transaction features
- **Task**: Detect fraudulent transactions
- **Source**: Synthetic (for demo)

### 4. **California Housing Prices** 🏠
- **Type**: Regression
- **Samples**: ~20,000
- **Features**: 8 housing characteristics
- **Task**: Predict median house value
- **Source**: sklearn

### 5. **Contract Classification** 📄
- **Type**: Multi-class Classification
- **Samples**: ~5,000
- **Features**: 6 contract characteristics
- **Task**: Classify contract type (lease, service, purchase, license)
- **Source**: Synthetic (FinQuery domain)

## Usage

### Load a Dataset

```python
from datasets.loaders import load_wine_quality

X_train, X_test, y_train, y_test = load_wine_quality()
print(f"Training samples: {len(X_train)}")
print(f"Test samples: {len(X_test)}")
```

### Train Models

```python
from datasets.train_models import train_all_models

# Train all models and register in model registry
results = train_all_models()
```

### List Available Datasets

```python
from datasets.loaders import list_available_datasets

datasets = list_available_datasets()
for name, info in datasets.items():
    print(f"{info['name']}: {info['description']}")
```

## Model Training

Models are automatically registered in the model registry with:
- Performance metrics (accuracy, F1, RMSE, R2)
- Hyperparameters
- Feature order
- Model metadata

## Integration with MLOps Platform

All trained models integrate with:
- ✅ Model Registry (versioning, lifecycle)
- ✅ Model Serving (real-time inference)
- ✅ A/B Testing (experiment framework)
- ✅ Model Monitoring (performance tracking)
- ✅ Experiment Tracking (MLflow-like)

## Showcase in Streamlit

Use the "📚 Datasets & Models" tab in the Streamlit UI to:
- Browse available datasets
- Load and explore datasets
- Train models interactively
- View registered models

---

**Perfect for demonstrating end-to-end ML capabilities!** 🚀

