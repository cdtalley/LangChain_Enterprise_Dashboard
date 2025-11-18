# 🚀 Quick Start Guide

## Getting Started

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/cdtalley/LangChain_Enterprise_Dashboard.git
cd LangChain_Enterprise_Dashboard

# Install dependencies (using pip)
pip install -r requirements.txt

# OR install using uv (recommended)
uv pip install -r requirements.txt
```

### 2. Start the Application

#### Option A: Streamlit UI (Recommended for demos)
```bash
streamlit run streamlit_app.py
```
Access at: http://localhost:8501

#### Option B: FastAPI Backend
```bash
uvicorn enterprise_features:app --reload --port 8000
```
API docs at: http://localhost:8000/docs

#### Option C: Docker Compose (Full stack)
```bash
docker-compose up --build
```

### 3. Key Features to Try

#### 🤖 Multi-Agent System
- Navigate to "Multi-Agent System" tab
- Try: "Research the latest trends in AI"
- Try: "Write Python code to analyze sales data"

#### 📊 Advanced RAG
- Upload a PDF document
- Ask questions about the document
- Try different retrieval strategies

#### 📦 Model Registry
- Register a new model
- Compare model versions
- View performance history

#### 🧪 A/B Testing
- Create an experiment
- Simulate experiment data
- Analyze results with statistical tests

#### 🔍 Model Monitoring
- Log performance metrics
- Detect data drift
- Generate monitoring reports

---

## Example Workflows

### Workflow 1: Document Processing Pipeline

```python
from document_processing import AdvancedDocumentProcessor

processor = AdvancedDocumentProcessor()

# Process a contract
result = processor.process_contract_document("lease.pdf")

# Extract structured data
structured_data = result['structured_data']
tables = result['tables']
```

### Workflow 2: AWS Bedrock Integration

```python
from aws_integration import AWSBedrockClient

bedrock = AWSBedrockClient(region_name="us-east-1")

# Use Claude for document analysis
response = bedrock.invoke_claude(
    prompt="Extract key terms from this contract...",
    model_id="anthropic.claude-v2"
)
```

### Workflow 3: Model Serving

```python
import requests

# Single prediction
response = requests.post(
    "http://localhost:8000/api/v1/models/predict",
    json={
        "features": {"feature1": 0.5, "feature2": 0.3},
        "model_name": "sentiment-classifier"
    }
)
```

### Workflow 4: A/B Testing

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
    min_sample_size=1000
)

exp_id = ab.create_experiment(config)
ab.start_experiment(exp_id)

# Record events
ab.record_event(exp_id, "user_123", 0.85)

# Analyze
results = ab.analyze_experiment(exp_id)
```

---

## Configuration

### Environment Variables

Create a `.env` file:

```bash
# AWS Configuration (optional)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret

# API Keys (optional)
OPENAI_API_KEY=your_key
SERPAPI_KEY=your_key

# Database
DATABASE_URL=sqlite:///enterprise_workbench.db
REDIS_URL=redis://localhost:6379/0
```

---

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Make sure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version: `python --version` (should be 3.11+)

2. **AWS Errors**
   - AWS features require credentials
   - Set up AWS credentials: `aws configure`
   - Or use environment variables

3. **Docker Build Fails**
   - Check Dockerfile exists
   - Verify all dependencies in requirements.txt

4. **Tests Fail**
   - Some tests may fail if optional dependencies are missing
   - Check the test output for specific errors

---

## Next Steps

1. **Explore Examples**: Check `examples/` directory
2. **Read Documentation**: See `README.md` and feature docs
3. **Try Integrations**: AWS, document processing, model serving
4. **Customize**: Modify configs for your use case

---

## Support

- **Documentation**: See `README.md`, `MLOPS_FEATURES.md`
- **Examples**: Check `examples/` directory
- **Issues**: GitHub Issues

