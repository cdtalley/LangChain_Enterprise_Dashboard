"""
Model Serving Example
=====================
Demonstrates production model serving with FastAPI.
"""

import requests
import json

def example_model_serving():
    """Example of using the model serving API"""
    
    base_url = "http://localhost:8000"
    
    print("🚀 Model Serving API Examples")
    print("=" * 50)
    
    # Example 1: Single prediction
    print("\n1️⃣ Single Prediction:")
    prediction_request = {
        "features": {
            "feature1": 0.75,
            "feature2": 0.45,
            "feature3": 0.82
        },
        "model_name": "sentiment-classifier",
        "return_probabilities": True
    }
    
    print(f"Request: {json.dumps(prediction_request, indent=2)}")
    print("\nTo call:")
    print(f"""
    response = requests.post(
        "{base_url}/api/v1/models/predict",
        json={json.dumps(prediction_request, indent=8)}
    )
    result = response.json()
    """)
    
    # Example 2: Batch prediction
    print("\n2️⃣ Batch Prediction:")
    batch_request = {
        "instances": [
            {"feature1": 0.75, "feature2": 0.45},
            {"feature1": 0.60, "feature2": 0.30},
            {"feature1": 0.90, "feature2": 0.80}
        ],
        "model_name": "sentiment-classifier"
    }
    
    print(f"Request: {json.dumps(batch_request, indent=2)}")
    print("\nTo call:")
    print(f"""
    response = requests.post(
        "{base_url}/api/v1/models/predict/batch",
        json={json.dumps(batch_request, indent=8)}
    )
    results = response.json()
    """)
    
    # Example 3: List available models
    print("\n3️⃣ List Available Models:")
    print(f"""
    response = requests.get("{base_url}/api/v1/models")
    models = response.json()
    print(models)
    """)
    
    # Example 4: Get model info
    print("\n4️⃣ Get Model Information:")
    print(f"""
    response = requests.get("{base_url}/api/v1/models/sentiment-classifier")
    model_info = response.json()
    print(model_info)
    """)


def example_integration_with_rag():
    """Example of integrating model serving with RAG"""
    
    print("\n🔗 Integration Example: RAG + Model Serving")
    print("=" * 50)
    
    example_code = """
    # 1. Process document with RAG
    from advanced_rag import AdvancedRAGSystem
    rag = AdvancedRAGSystem()
    rag.load_document("contract.pdf", "pdf")
    
    # 2. Query document
    results = rag.query_documents("What is the monthly rent?")
    
    # 3. Use extracted information for model prediction
    import requests
    prediction = requests.post(
        "http://localhost:8000/api/v1/models/predict",
        json={
            "features": {
                "rent_amount": extract_rent(results['answer']),
                "lease_term": extract_term(results['answer'])
            },
            "model_name": "lease-risk-classifier"
        }
    )
    """
    
    print(example_code)


if __name__ == "__main__":
    example_model_serving()
    example_integration_with_rag()

