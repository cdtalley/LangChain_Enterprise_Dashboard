"""
AWS Bedrock Integration Example
================================
Demonstrates AWS Bedrock usage for LLM services.
"""

from aws_integration import AWSBedrockClient
import json

def example_bedrock_usage():
    """Example of using AWS Bedrock for LLM services"""
    
    # Initialize Bedrock client
    bedrock = AWSBedrockClient(region_name="us-east-1")
    
    # List available models
    print("Available Bedrock models:")
    models = bedrock.list_available_models()
    for model in models[:5]:  # Show first 5
        print(f"  - {model.get('modelId', 'N/A')}: {model.get('modelName', 'N/A')}")
    
    # Example: Extract contract terms using Claude
    contract_text = """
    This lease agreement is between ABC Properties (Lessor) and XYZ Corp (Lessee).
    The property is located at 123 Main St, Atlanta, GA.
    Lease term: January 1, 2024 to December 31, 2026.
    Monthly rent: $5,000. Security deposit: $10,000.
    """
    
    extraction_prompt = f"""
    Extract key information from this lease agreement:
    
    {contract_text}
    
    Extract:
    - Lessor name
    - Lessee name
    - Property address
    - Lease start date
    - Lease end date
    - Monthly rent
    - Security deposit
    
    Return as JSON.
    """
    
    try:
        response = bedrock.invoke_claude(
            prompt=extraction_prompt,
            model_id="anthropic.claude-v2",
            max_tokens=500,
            temperature=0.1  # Low temperature for structured extraction
        )
        
        print("\n✅ Claude Response:")
        print(response['text'])
        print(f"\nUsage: {response['usage']}")
        
    except Exception as e:
        print(f"⚠️ Note: AWS credentials required. Error: {e}")
        print("This example demonstrates the integration pattern.")


if __name__ == "__main__":
    example_bedrock_usage()

