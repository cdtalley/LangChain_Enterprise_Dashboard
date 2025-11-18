"""
AWS AI/ML Integration
=====================
AWS Bedrock, SageMaker, and S3 integration for production ML.
Demonstrates AWS AI/ML stack experience.
"""

import boto3
import json
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AWSBedrockClient:
    """
    AWS Bedrock Integration for LLM Services
    
    Supports:
    - Claude (Anthropic)
    - Llama 2
    - Titan
    - Jurassic-2
    """
    
    def __init__(self, region_name: str = "us-east-1"):
        self.bedrock_runtime = boto3.client(
            'bedrock-runtime',
            region_name=region_name
        )
        self.bedrock = boto3.client('bedrock', region_name=region_name)
        self.region = region_name
        logger.info(f"AWS Bedrock client initialized for region {region_name}")
    
    def list_available_models(self) -> List[Dict[str, Any]]:
        """List available foundation models"""
        try:
            response = self.bedrock.list_foundation_models()
            return response.get('modelSummaries', [])
        except ClientError as e:
            logger.error(f"Error listing models: {e}")
            return []
    
    def invoke_claude(
        self,
        prompt: str,
        model_id: str = "anthropic.claude-v2",
        max_tokens: int = 1000,
        temperature: float = 0.7,
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Invoke Claude model via Bedrock
        
        Args:
            prompt: User prompt
            model_id: Bedrock model ID
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            system_prompt: Optional system prompt
            
        Returns:
            Response dictionary with generated text
        """
        try:
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            if system_prompt:
                body["system"] = system_prompt
            
            response = self.bedrock_runtime.invoke_model(
                modelId=model_id,
                body=json.dumps(body)
            )
            
            response_body = json.loads(response['body'].read())
            
            return {
                "text": response_body.get('content', [{}])[0].get('text', ''),
                "model_id": model_id,
                "usage": response_body.get('usage', {}),
                "stop_reason": response_body.get('stop_reason', '')
            }
            
        except ClientError as e:
            logger.error(f"Error invoking Claude: {e}")
            raise
    
    def invoke_llama(
        self,
        prompt: str,
        model_id: str = "meta.llama2-70b-chat-v1",
        max_tokens: int = 512,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Invoke Llama 2 model via Bedrock"""
        try:
            body = {
                "prompt": prompt,
                "max_gen_len": max_tokens,
                "temperature": temperature
            }
            
            response = self.bedrock_runtime.invoke_model(
                modelId=model_id,
                body=json.dumps(body)
            )
            
            response_body = json.loads(response['body'].read())
            
            return {
                "text": response_body.get('generation', ''),
                "model_id": model_id,
                "stop_reason": response_body.get('stop_reason', '')
            }
            
        except ClientError as e:
            logger.error(f"Error invoking Llama: {e}")
            raise


class AWSS3ModelStorage:
    """S3 integration for model storage and retrieval"""
    
    def __init__(self, bucket_name: str, region_name: str = "us-east-1"):
        self.s3 = boto3.client('s3', region_name=region_name)
        self.bucket_name = bucket_name
        logger.info(f"S3 client initialized for bucket {bucket_name}")
    
    def upload_model(
        self,
        model_path: str,
        s3_key: str,
        metadata: Optional[Dict[str, str]] = None
    ) -> str:
        """Upload model file to S3"""
        try:
            extra_args = {}
            if metadata:
                extra_args['Metadata'] = metadata
            
            self.s3.upload_file(
                model_path,
                self.bucket_name,
                s3_key,
                ExtraArgs=extra_args
            )
            
            s3_url = f"s3://{self.bucket_name}/{s3_key}"
            logger.info(f"Model uploaded to {s3_url}")
            return s3_url
            
        except ClientError as e:
            logger.error(f"Error uploading model: {e}")
            raise
    
    def download_model(self, s3_key: str, local_path: str):
        """Download model from S3"""
        try:
            self.s3.download_file(
                self.bucket_name,
                s3_key,
                local_path
            )
            logger.info(f"Model downloaded from s3://{self.bucket_name}/{s3_key}")
        except ClientError as e:
            logger.error(f"Error downloading model: {e}")
            raise
    
    def list_models(self, prefix: str = "models/") -> List[Dict[str, Any]]:
        """List all models in S3"""
        try:
            response = self.s3.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix
            )
            
            models = []
            for obj in response.get('Contents', []):
                models.append({
                    'key': obj['Key'],
                    'size': obj['Size'],
                    'last_modified': obj['LastModified'].isoformat(),
                    'url': f"s3://{self.bucket_name}/{obj['Key']}"
                })
            
            return models
        except ClientError as e:
            logger.error(f"Error listing models: {e}")
            return []


class AWSSageMakerDeployment:
    """SageMaker model deployment"""
    
    def __init__(self, region_name: str = "us-east-1"):
        self.sagemaker = boto3.client('sagemaker', region_name=region_name)
        self.region = region_name
        logger.info(f"SageMaker client initialized for region {region_name}")
    
    def create_model(
        self,
        model_name: str,
        model_s3_path: str,
        execution_role_arn: str,
        container_image: str
    ) -> str:
        """Create SageMaker model"""
        try:
            response = self.sagemaker.create_model(
                ModelName=model_name,
                PrimaryContainer={
                    'Image': container_image,
                    'ModelDataUrl': model_s3_path
                },
                ExecutionRoleArn=execution_role_arn
            )
            
            logger.info(f"Model {model_name} created in SageMaker")
            return response['ModelArn']
            
        except ClientError as e:
            logger.error(f"Error creating model: {e}")
            raise
    
    def create_endpoint_config(
        self,
        config_name: str,
        model_name: str,
        instance_type: str = "ml.m5.large",
        initial_instance_count: int = 1
    ) -> str:
        """Create endpoint configuration"""
        try:
            response = self.sagemaker.create_endpoint_config(
                EndpointConfigName=config_name,
                ProductionVariants=[{
                    'VariantName': 'AllTraffic',
                    'ModelName': model_name,
                    'InstanceType': instance_type,
                    'InitialInstanceCount': initial_instance_count,
                    'InitialVariantWeight': 1
                }]
            )
            
            logger.info(f"Endpoint config {config_name} created")
            return response['EndpointConfigArn']
            
        except ClientError as e:
            logger.error(f"Error creating endpoint config: {e}")
            raise
    
    def create_endpoint(
        self,
        endpoint_name: str,
        config_name: str
    ) -> str:
        """Create SageMaker endpoint"""
        try:
            response = self.sagemaker.create_endpoint(
                EndpointName=endpoint_name,
                EndpointConfigName=config_name
            )
            
            logger.info(f"Endpoint {endpoint_name} created")
            return response['EndpointArn']
            
        except ClientError as e:
            logger.error(f"Error creating endpoint: {e}")
            raise


class AWSTextractProcessor:
    """AWS Textract for document processing"""
    
    def __init__(self, region_name: str = "us-east-1"):
        self.textract = boto3.client('textract', region_name=region_name)
        self.region = region_name
        logger.info(f"Textract client initialized for region {region_name}")
    
    def extract_text(self, s3_bucket: str, s3_key: str) -> Dict[str, Any]:
        """Extract text from document in S3"""
        try:
            response = self.textract.detect_document_text(
                Document={
                    'S3Object': {
                        'Bucket': s3_bucket,
                        'Name': s3_key
                    }
                }
            )
            
            # Extract text blocks
            text_blocks = []
            for block in response.get('Blocks', []):
                if block['BlockType'] == 'LINE':
                    text_blocks.append(block['Text'])
            
            return {
                'text': '\n'.join(text_blocks),
                'blocks': response.get('Blocks', []),
                'document_metadata': response.get('DocumentMetadata', {})
            }
            
        except ClientError as e:
            logger.error(f"Error extracting text: {e}")
            raise
    
    def extract_tables(self, s3_bucket: str, s3_key: str) -> Dict[str, Any]:
        """Extract tables from document"""
        try:
            response = self.textract.analyze_document(
                Document={
                    'S3Object': {
                        'Bucket': s3_bucket,
                        'Name': s3_key
                    }
                },
                FeatureTypes=['TABLES']
            )
            
            # Process table blocks
            tables = []
            for block in response.get('Blocks', []):
                if block['BlockType'] == 'TABLE':
                    tables.append(block)
            
            return {
                'tables': tables,
                'blocks': response.get('Blocks', []),
                'document_metadata': response.get('DocumentMetadata', {})
            }
            
        except ClientError as e:
            logger.error(f"Error extracting tables: {e}")
            raise
    
    def analyze_document(
        self,
        s3_bucket: str,
        s3_key: str,
        feature_types: List[str] = ['TABLES', 'FORMS']
    ) -> Dict[str, Any]:
        """Comprehensive document analysis"""
        try:
            response = self.textract.analyze_document(
                Document={
                    'S3Object': {
                        'Bucket': s3_bucket,
                        'Name': s3_key
                    }
                },
                FeatureTypes=feature_types
            )
            
            return {
                'blocks': response.get('Blocks', []),
                'document_metadata': response.get('DocumentMetadata', {}),
                'analyze_document_model_version': response.get('AnalyzeDocumentModelVersion', '')
            }
            
        except ClientError as e:
            logger.error(f"Error analyzing document: {e}")
            raise

