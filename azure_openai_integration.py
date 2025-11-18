"""
Azure OpenAI Integration
========================
Production-ready Azure OpenAI service integration.
Demonstrates cloud-native Gen AI expertise.
"""

import os
from typing import Dict, Any, Optional, List
import logging
from dataclasses import dataclass

try:
    from openai import AzureOpenAI
    AZURE_OPENAI_AVAILABLE = True
except ImportError:
    AZURE_OPENAI_AVAILABLE = False
    logging.warning("openai package required. Install with: pip install openai")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class AzureOpenAIConfig:
    """Azure OpenAI configuration"""
    api_key: str
    endpoint: str
    api_version: str = "2024-02-15-preview"
    deployment_name: str = "gpt-4"


class AzureOpenAIClient:
    """
    Azure OpenAI client for Gen AI applications
    
    Features:
    - Chat completions (GPT-4, GPT-3.5)
    - Embeddings
    - Function calling
    - Streaming responses
    - Error handling and retries
    """
    
    def __init__(self, config: AzureOpenAIConfig):
        if not AZURE_OPENAI_AVAILABLE:
            raise ImportError("openai package required for Azure OpenAI")
        
        self.config = config
        self.client = AzureOpenAI(
            api_key=config.api_key,
            api_version=config.api_version,
            azure_endpoint=config.endpoint
        )
        logger.info(f"Azure OpenAI client initialized for deployment: {config.deployment_name}")
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        stream: bool = False,
        functions: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """Chat completion with Azure OpenAI"""
        try:
            params = {
                "model": self.config.deployment_name,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": stream
            }
            
            if functions:
                params["functions"] = functions
            
            response = self.client.chat.completions.create(**params)
            
            if stream:
                return {"stream": response}
            
            return {
                "text": response.choices[0].message.content,
                "role": response.choices[0].message.role,
                "finish_reason": response.choices[0].finish_reason,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
        except Exception as e:
            logger.error(f"Azure OpenAI chat completion failed: {e}")
            raise
    
    def get_embeddings(self, text: str, model: str = "text-embedding-ada-002") -> List[float]:
        """Get embeddings from Azure OpenAI"""
        try:
            response = self.client.embeddings.create(
                model=model,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Azure OpenAI embeddings failed: {e}")
            raise
    
    def batch_embeddings(self, texts: List[str], model: str = "text-embedding-ada-002") -> List[List[float]]:
        """Get embeddings for multiple texts"""
        try:
            response = self.client.embeddings.create(
                model=model,
                input=texts
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            logger.error(f"Azure OpenAI batch embeddings failed: {e}")
            raise


def create_azure_client(
    api_key: Optional[str] = None,
    endpoint: Optional[str] = None,
    deployment_name: str = "gpt-4"
) -> AzureOpenAIClient:
    """Create Azure OpenAI client from environment or parameters"""
    api_key = api_key or os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
    
    if not api_key or not endpoint:
        raise ValueError("Azure OpenAI API key and endpoint required")
    
    config = AzureOpenAIConfig(
        api_key=api_key,
        endpoint=endpoint,
        deployment_name=deployment_name
    )
    
    return AzureOpenAIClient(config)

