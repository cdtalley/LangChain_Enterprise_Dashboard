# 🔗 Integration Guide

## AWS Integration

### Setup AWS Credentials

```bash
# Option 1: AWS CLI
aws configure

# Option 2: Environment Variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-east-1
```

### Using AWS Bedrock

```python
from aws_integration import AWSBedrockClient

# Initialize client
bedrock = AWSBedrockClient(region_name="us-east-1")

# List available models
models = bedrock.list_available_models()

# Invoke Claude
response = bedrock.invoke_claude(
    prompt="Analyze this contract...",
    model_id="anthropic.claude-v2",
    max_tokens=1000
)

print(response['text'])
```

### Using AWS S3 for Model Storage

```python
from aws_integration import AWSS3ModelStorage

# Initialize S3 storage
s3_storage = AWSS3ModelStorage(
    bucket_name="my-models-bucket",
    region_name="us-east-1"
)

# Upload model
s3_url = s3_storage.upload_model(
    model_path="./models/model.pkl",
    s3_key="models/sentiment-classifier/v1.0.0/model.pkl",
    metadata={"version": "1.0.0", "author": "Data Scientist"}
)

# Download model
s3_storage.download_model(
    s3_key="models/sentiment-classifier/v1.0.0/model.pkl",
    local_path="./downloaded_model.pkl"
)
```

### Using AWS Textract for Document Processing

```python
from aws_integration import AWSTextractProcessor

# Initialize Textract
textract = AWSTextractProcessor(region_name="us-east-1")

# Extract text from S3 document
result = textract.extract_text(
    s3_bucket="my-documents-bucket",
    s3_key="contracts/lease-001.pdf"
)

# Extract tables
tables = textract.extract_tables(
    s3_bucket="my-documents-bucket",
    s3_key="contracts/lease-001.pdf"
)
```

---

## Document Processing Integration

### Basic Document Processing

```python
from document_processing import AdvancedDocumentProcessor

processor = AdvancedDocumentProcessor()

# Process contract
result = processor.process_contract_document(
    "lease.pdf",
    extract_tables=True,
    use_ocr=False
)

# Access results
text = result['text']
tables = result['tables']
structured_data = result['structured_data']
```

### Extract Tables from PDF

```python
tables = processor.extract_tables_from_pdf("lease.pdf")

for table in tables:
    print(f"Table on page {table['page']}:")
    df = table['dataframe']
    print(df)
```

### OCR for Scanned Documents

```python
ocr_result = processor.extract_text_with_ocr("scanned_contract.png")

print(f"Extracted text: {ocr_result['text']}")
print(f"Confidence: {ocr_result.get('confidence_scores', [])}")
```

### Lease-Specific Extraction

```python
lease_data = processor.extract_lease_terms("lease.pdf")

print(lease_data['lease_terms'])
print(lease_data['full_document'])
```

---

## Context Engineering Integration

### Few-Shot Learning

```python
from context_engineering import ContextEngineer, FewShotExample

engineer = ContextEngineer()

# Create examples
examples = [
    FewShotExample(
        input_text="Lease term: 3 years. Rent: $5,000/month.",
        output_text='{"term_years": 3, "monthly_rent": 5000}'
    )
]

# Build prompt
prompt = engineer.build_few_shot_prompt(
    examples=examples,
    task_description="Extract structured data from lease documents",
    user_input="Lease: 2 years, $3,500/month"
)
```

### Chain-of-Thought Prompting

```python
prompt = engineer.build_chain_of_thought_prompt(
    question="What is the total lease cost?",
    reasoning_steps=[
        "Calculate monthly rent × number of months",
        "Add security deposit",
        "Sum all costs"
    ]
)
```

### RAG Optimization

```python
prompt = engineer.create_rag_prompt(
    query="What are the key lease terms?",
    context=document_text,
    system_instruction="You are a legal document analyst."
)
```

---

## Model Serving Integration

### FastAPI Endpoints

```python
import requests

BASE_URL = "http://localhost:8000"

# Single prediction
response = requests.post(
    f"{BASE_URL}/api/v1/models/predict",
    json={
        "features": {"feature1": 0.5, "feature2": 0.3},
        "model_name": "sentiment-classifier",
        "return_probabilities": True
    }
)

result = response.json()
print(f"Prediction: {result['prediction']}")
print(f"Probabilities: {result['probabilities']}")
```

### Batch Predictions

```python
response = requests.post(
    f"{BASE_URL}/api/v1/models/predict/batch",
    json={
        "instances": [
            {"feature1": 0.5, "feature2": 0.3},
            {"feature1": 0.7, "feature2": 0.1}
        ],
        "model_name": "sentiment-classifier"
    }
)

results = response.json()
print(f"Predictions: {results['predictions']}")
```

---

## Complete Integration Example

```python
"""
Complete workflow: Document → RAG → Model Serving → Monitoring
"""

from document_processing import AdvancedDocumentProcessor
from advanced_rag import AdvancedRAGSystem
from model_registry import ModelRegistryManager
from model_monitoring import ModelMonitoring
import requests

# 1. Process document
processor = AdvancedDocumentProcessor()
doc_result = processor.process_contract_document("lease.pdf")

# 2. Extract structured data using RAG
rag = AdvancedRAGSystem()
rag.load_document("lease.pdf", "pdf")
rag_result = rag.query_documents("What is the monthly rent and lease term?")

# 3. Prepare features for model
features = {
    "rent_amount": extract_rent(rag_result['answer']),
    "lease_term_months": extract_term_months(rag_result['answer']),
    "property_type": "commercial"
}

# 4. Get prediction from model serving API
response = requests.post(
    "http://localhost:8000/api/v1/models/predict",
    json={
        "features": features,
        "model_name": "lease-risk-classifier"
    }
)

prediction = response.json()

# 5. Log performance for monitoring
monitoring = ModelMonitoring()
monitoring.log_performance(
    model_name="lease-risk-classifier",
    model_version="1.0.0",
    metric_name="prediction_confidence",
    metric_value=prediction.get('probabilities', {}).get('high_risk', 0),
    prediction_count=1
)

print(f"Risk prediction: {prediction['prediction']}")
print(f"Confidence: {prediction.get('probabilities', {})}")
```

---

## Environment Setup

### Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export AWS_REGION=us-east-1
export DATABASE_URL=sqlite:///dev.db

# Run tests
pytest tests/ -v
```

### Production

```bash
# Use Docker
docker-compose up -d

# Or deploy to Kubernetes
kubectl apply -f deployment/kubernetes/deployment.yaml
```

---

## Best Practices

1. **Error Handling**: Always wrap AWS calls in try/except
2. **Caching**: Use feature store for frequently accessed features
3. **Monitoring**: Log all predictions for monitoring
4. **Validation**: Validate inputs before model serving
5. **Security**: Never commit AWS credentials

---

For more examples, see the `examples/` directory.

