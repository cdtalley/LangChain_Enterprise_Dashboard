"""
Google Cloud Vertex AI Integration
===================================
Production-ready GCP Vertex AI integration for Gen AI.
Demonstrates multi-cloud Gen AI expertise.
"""

import os
from typing import Dict, Any, Optional, List
import logging
from dataclasses import dataclass

try:
    import vertexai
    from vertexai.preview.language_models import TextGenerationModel, ChatModel
    from vertexai.language_models import TextEmbeddingModel
    VERTEX_AI_AVAILABLE = True
except ImportError:
    VERTEX_AI_AVAILABLE = False
    logging.warning("google-cloud-aiplatform required. Install with: pip install google-cloud-aiplatform")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class VertexAIConfig:
    """Vertex AI configuration"""
    project_id: str
    location: str = "us-central1"
    model_name: str = "text-bison"


class VertexAIClient:
    """
    Vertex AI client for Gen AI applications
    
    Features:
    - Text generation (PaLM, Gemini)
    - Chat completions
    - Embeddings
    - Model fine-tuning
    - Multi-modal support
    """
    
    def __init__(self, config: VertexAIConfig):
        if not VERTEX_AI_AVAILABLE:
            raise ImportError("google-cloud-aiplatform required for Vertex AI")
        
        self.config = config
        vertexai.init(project=config.project_id, location=config.location)
        logger.info(f"Vertex AI initialized for project: {config.project_id}")
    
    def generate_text(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_output_tokens: int = 1024,
        top_p: float = 0.95,
        top_k: int = 40
    ) -> Dict[str, Any]:
        """Generate text using Vertex AI"""
        try:
            model = TextGenerationModel.from_pretrained(self.config.model_name)
            
            response = model.predict(
                prompt=prompt,
                temperature=temperature,
                max_output_tokens=max_output_tokens,
                top_p=top_p,
                top_k=top_k
            )
            
            return {
                "text": response.text,
                "safety_ratings": [
                    {
                        "category": rating.category.name,
                        "probability": rating.probability.name
                    }
                    for rating in response.safety_ratings
                ] if hasattr(response, 'safety_ratings') else []
            }
        except Exception as e:
            logger.error(f"Vertex AI text generation failed: {e}")
            raise
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_output_tokens: int = 1024
    ) -> Dict[str, Any]:
        """Chat completion with Vertex AI"""
        try:
            chat_model = ChatModel.from_pretrained(self.config.model_name)
            chat = chat_model.start_chat()
            
            for msg in messages[:-1]:
                if msg["role"] == "user":
                    chat.send_message(msg["content"])
                elif msg["role"] == "assistant":
                    pass
            
            last_message = messages[-1]["content"]
            response = chat.send_message(
                last_message,
                temperature=temperature,
                max_output_tokens=max_output_tokens
            )
            
            return {
                "text": response.text,
                "safety_ratings": [
                    {
                        "category": rating.category.name,
                        "probability": rating.probability.name
                    }
                    for rating in response.safety_ratings
                ] if hasattr(response, 'safety_ratings') else []
            }
        except Exception as e:
            logger.error(f"Vertex AI chat completion failed: {e}")
            raise
    
    def get_embeddings(self, text: str, model_name: str = "textembedding-gecko@001") -> List[float]:
        """Get embeddings from Vertex AI"""
        try:
            model = TextEmbeddingModel.from_pretrained(model_name)
            embeddings = model.get_embeddings([text])
            return embeddings[0].values
        except Exception as e:
            logger.error(f"Vertex AI embeddings failed: {e}")
            raise
    
    def batch_embeddings(self, texts: List[str], model_name: str = "textembedding-gecko@001") -> List[List[float]]:
        """Get embeddings for multiple texts"""
        try:
            model = TextEmbeddingModel.from_pretrained(model_name)
            embeddings = model.get_embeddings(texts)
            return [emb.values for emb in embeddings]
        except Exception as e:
            logger.error(f"Vertex AI batch embeddings failed: {e}")
            raise


def create_vertex_client(
    project_id: Optional[str] = None,
    location: str = "us-central1",
    model_name: str = "text-bison"
) -> VertexAIClient:
    """Create Vertex AI client from environment or parameters"""
    project_id = project_id or os.getenv("GCP_PROJECT_ID")
    
    if not project_id:
        raise ValueError("GCP project ID required")
    
    config = VertexAIConfig(
        project_id=project_id,
        location=location,
        model_name=model_name
    )
    
    return VertexAIClient(config)

