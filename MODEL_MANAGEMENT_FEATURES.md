# 🎯 Model Management & A/B Testing Features

## Overview

This project now showcases **advanced Python and MLOps capabilities** through a comprehensive model management and experimentation platform. These features demonstrate production-ready skills in:

- **Model Versioning & Registry**
- **A/B Testing with Statistical Significance**
- **Experiment Tracking (MLflow-like)**
- **Model Performance Monitoring & Drift Detection**

---

## 📦 Model Registry System (`model_registry.py`)

### Key Features:
- **Model Versioning**: Track multiple versions of models with semantic versioning
- **Lifecycle Management**: Development → Staging → Production → Archived
- **Metadata Tracking**: Performance metrics, hyperparameters, dependencies, tags
- **Model Comparison**: Side-by-side comparison of model versions
- **Performance History**: Track performance metrics over time

### Python Skills Demonstrated:
- ✅ **Advanced OOP**: Dataclasses, Enums, Type hints
- ✅ **Database Design**: SQLAlchemy ORM with proper relationships
- ✅ **Serialization**: Model persistence with joblib/pickle
- ✅ **Metadata Management**: JSON-based flexible metadata storage
- ✅ **File System Operations**: Organized model storage structure

### Example Usage:
```python
from model_registry import ModelRegistryManager, ModelType, ModelStage

registry = ModelRegistryManager()

# Register a model
model_id = registry.register_model(
    model=trained_model,
    name="sentiment-classifier",
    version="1.0.0",
    model_type=ModelType.CLASSIFIER,
    performance_metrics={"accuracy": 0.92, "f1": 0.89},
    hyperparameters={"learning_rate": 0.001, "epochs": 10},
    stage=ModelStage.PRODUCTION
)

# Compare versions
comparison = registry.compare_models("sentiment-classifier", "1.0.0", "1.1.0")
```

---

## 🧪 A/B Testing Framework (`ab_testing.py`)

### Key Features:
- **Statistical Testing**: t-test, chi-square, Mann-Whitney U test
- **Traffic Splitting**: Consistent hashing for user assignment
- **Sample Size Calculation**: Power analysis for experiment design
- **Early Stopping**: Futility and success detection
- **Effect Size Analysis**: Relative lift and absolute differences

### Python Skills Demonstrated:
- ✅ **Statistical Analysis**: scipy.stats integration
- ✅ **Hypothesis Testing**: Proper p-value interpretation
- ✅ **Experiment Design**: Power analysis and sample size calculation
- ✅ **Data Structures**: Efficient event tracking and aggregation
- ✅ **Statistical Rigor**: Multiple test types for different metric types

### Statistical Tests Implemented:
1. **Continuous Metrics**: Two-sample t-test
2. **Binary Metrics**: Chi-square test for proportions
3. **Count Metrics**: Mann-Whitney U test (non-parametric)

### Example Usage:
```python
from ab_testing import ABTestingFramework, ExperimentConfig, MetricType

ab = ABTestingFramework()

# Create experiment
config = ExperimentConfig(
    name="model-v2-test",
    metric_name="accuracy",
    metric_type=MetricType.CONTINUOUS,
    baseline_model="model-v1",
    treatment_model="model-v2",
    traffic_split=0.5,
    min_sample_size=1000,
    significance_level=0.05
)
exp_id = ab.create_experiment(config)

# Record events
ab.record_event(exp_id, "user_123", 0.85)

# Analyze results
results = ab.analyze_experiment(exp_id)
# Returns: p-value, statistical significance, effect size, recommendation
```

---

## 📝 Experiment Tracking (`experiment_tracking.py`)

### Key Features:
- **Run Tracking**: Start/stop experiment runs with metadata
- **Parameter Logging**: Track hyperparameters and configuration
- **Metric Logging**: Time-series metric tracking with steps
- **Artifact Storage**: Store model files, plots, and other artifacts
- **Run Comparison**: Compare multiple runs side-by-side

### Python Skills Demonstrated:
- ✅ **MLflow-like API**: Familiar interface for ML practitioners
- ✅ **Time-series Data**: Metric history tracking
- ✅ **Artifact Management**: File system organization
- ✅ **Data Analysis**: Pandas integration for run comparison
- ✅ **Flexible Storage**: JSON-based flexible metadata

### Example Usage:
```python
from experiment_tracking import ExperimentTracking

tracking = ExperimentTracking()

# Start run
run_id = tracking.start_run("model-training", "run-001")

# Log parameters
tracking.log_params(run_id, {"learning_rate": 0.001, "batch_size": 32})

# Log metrics over time
for epoch in range(10):
    tracking.log_metrics(run_id, {"accuracy": accuracy}, step=epoch)

# Compare runs
comparison_df = tracking.compare_runs([run_id1, run_id2])
```

---

## 🔍 Model Monitoring (`model_monitoring.py`)

### Key Features:
- **Performance Tracking**: Real-time metric logging
- **Data Drift Detection**: Kolmogorov-Smirnov test and PSI
- **Performance Drift**: Statistical process control charts
- **Anomaly Detection**: Control limits and trend analysis
- **Comprehensive Reports**: Multi-metric analysis

### Python Skills Demonstrated:
- ✅ **Statistical Process Control**: Control charts and limits
- ✅ **Drift Detection**: KS test, Population Stability Index (PSI)
- ✅ **Time-series Analysis**: Trend detection with linear regression
- ✅ **Anomaly Detection**: Multi-sigma rule implementation
- ✅ **Data Analysis**: Comprehensive reporting with pandas

### Detection Methods:
1. **Data Drift**: KS test + PSI for feature distribution changes
2. **Performance Drift**: Control charts with 3-sigma limits
3. **Trend Detection**: Linear regression for degradation detection

### Example Usage:
```python
from model_monitoring import ModelMonitoring

monitoring = ModelMonitoring()

# Log performance
monitoring.log_performance(
    "sentiment-classifier", "1.0.0", "accuracy", 0.92, prediction_count=1000
)

# Detect drift
drift_results = monitoring.detect_performance_drift(
    "sentiment-classifier", "1.0.0", "accuracy", lookback_days=7
)

# Generate report
report = monitoring.generate_monitoring_report(
    "sentiment-classifier", "1.0.0", days=30
)
```

---

## 🎨 Streamlit UI Integration

### New Tabs Added:
1. **📦 Model Registry**: Register, compare, and manage models
2. **🧪 A/B Testing**: Create experiments, analyze results, calculate sample sizes
3. **📝 Experiment Tracking**: Track training runs with parameters and metrics
4. **🔍 Model Monitoring**: Monitor performance and detect drift

### UI Features:
- Interactive model registration forms
- Real-time experiment analysis
- Visual performance trends (Plotly charts)
- Statistical test results display
- Model comparison interfaces

---

## 💼 Skills Showcased for Hiring

### **Python Expertise**:
- ✅ Advanced OOP patterns (dataclasses, enums, type hints)
- ✅ Database design with SQLAlchemy ORM
- ✅ Statistical analysis with scipy
- ✅ Data manipulation with pandas/numpy
- ✅ File system operations and serialization
- ✅ Clean, maintainable code structure

### **MLOps Capabilities**:
- ✅ Model versioning and lifecycle management
- ✅ Experiment tracking and comparison
- ✅ A/B testing with statistical rigor
- ✅ Performance monitoring and alerting
- ✅ Drift detection and anomaly detection
- ✅ Production-ready monitoring systems

### **Statistical Knowledge**:
- ✅ Hypothesis testing (t-test, chi-square, Mann-Whitney)
- ✅ Power analysis and sample size calculation
- ✅ Effect size calculation and interpretation
- ✅ Statistical process control
- ✅ Drift detection methods (KS test, PSI)

### **Production Engineering**:
- ✅ Database design and optimization
- ✅ Efficient data structures
- ✅ Error handling and logging
- ✅ Scalable architecture
- ✅ API design (FastAPI integration ready)

---

## 🚀 How to Use

### 1. Start Streamlit App:
```bash
streamlit run streamlit_app.py
```

### 2. Navigate to Model Management Tabs:
- **Model Registry**: Register and compare models
- **A/B Testing**: Create and analyze experiments
- **Experiment Tracking**: Track training runs
- **Model Monitoring**: Monitor production models

### 3. Example Workflow:

1. **Train a model** → Register in Model Registry
2. **Create A/B test** → Compare baseline vs treatment
3. **Track experiments** → Log parameters and metrics
4. **Monitor production** → Detect drift and degradation

---

## 📊 Key Metrics Tracked

- **Model Performance**: Accuracy, precision, recall, F1
- **Experiment Metrics**: Statistical significance, effect size, sample size
- **Monitoring Metrics**: Drift scores, violation rates, trends
- **System Metrics**: Model size, prediction counts, timestamps

---

## 🎯 Perfect For These Roles

- **Senior Data Scientist**: Advanced Python + MLOps
- **ML Engineer**: Model management and experimentation
- **MLOps Engineer**: Production monitoring and deployment
- **Research Scientist**: Experiment tracking and analysis

---

## 📈 Next Steps

To further enhance:
1. Add FastAPI endpoints for model serving
2. Integrate with cloud storage (S3, GCS)
3. Add model deployment automation
4. Integrate with MLflow or Weights & Biases
5. Add real-time alerting (email, Slack)

---

**This demonstrates enterprise-grade Python and MLOps capabilities that are immediately applicable in production environments.**

