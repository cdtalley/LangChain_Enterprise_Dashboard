"""
Enhanced Configuration for Enterprise LangChain AI Workbench
===========================================================
Centralized configuration management for all application components.
"""

import os
from typing import Dict, Any, Optional
from pathlib import Path

class Config:
    """Centralized configuration management"""
    
    # Application Settings
    APP_NAME = "Enterprise LangChain AI Workbench"
    APP_VERSION = "2.1.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # API Configuration
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", "8501"))
    
    # Database Configuration
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///enterprise_workbench.db")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # AI Model Configuration
    DEFAULT_LLM_MODEL = os.getenv("DEFAULT_LLM_MODEL", "microsoft/DialoGPT-medium")
    FALLBACK_LLM_MODEL = os.getenv("FALLBACK_LLM_MODEL", "gpt2")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "512"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    
    # Performance Settings
    CACHE_TTL = int(os.getenv("CACHE_TTL", "300"))  # 5 minutes
    MAX_CONCURRENT_QUERIES = int(os.getenv("MAX_CONCURRENT_QUERIES", "10"))
    QUERY_TIMEOUT = int(os.getenv("QUERY_TIMEOUT", "30"))  # seconds
    
    # Security Settings
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRATION_HOURS = 24
    
    # Monitoring Settings
    ENABLE_METRICS = os.getenv("ENABLE_METRICS", "True").lower() == "true"
    METRICS_RETENTION_DAYS = int(os.getenv("METRICS_RETENTION_DAYS", "30"))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # RAG Configuration
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
    MAX_DOCUMENTS = int(os.getenv("MAX_DOCUMENTS", "1000"))
    SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.7"))
    
    # Agent Configuration
    AGENT_MEMORY_SIZE = int(os.getenv("AGENT_MEMORY_SIZE", "20"))
    ENABLE_AUTO_ROUTING = os.getenv("ENABLE_AUTO_ROUTING", "True").lower() == "true"
    ROUTING_CONFIDENCE_THRESHOLD = float(os.getenv("ROUTING_CONFIDENCE_THRESHOLD", "0.6"))
    
    # File Upload Settings
    MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
    ALLOWED_FILE_TYPES = ["pdf", "txt", "docx", "md"]
    UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "uploads"))
    
    # External API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SERPAPI_KEY = os.getenv("SERPAPI_KEY")
    
    @classmethod
    def get_database_config(cls) -> Dict[str, Any]:
        """Get database configuration"""
        return {
            "url": cls.DATABASE_URL,
            "echo": cls.DEBUG,
            "pool_pre_ping": True,
            "pool_recycle": 300
        }
    
    @classmethod
    def get_redis_config(cls) -> Dict[str, Any]:
        """Get Redis configuration"""
        return {
            "url": cls.REDIS_URL,
            "decode_responses": True,
            "socket_keepalive": True,
            "socket_keepalive_options": {}
        }
    
    @classmethod
    def get_llm_config(cls) -> Dict[str, Any]:
        """Get LLM configuration"""
        try:
            import torch
            use_gpu = torch.cuda.is_available()
        except ImportError:
            use_gpu = False
            
        return {
            "model_name": cls.DEFAULT_LLM_MODEL,
            "fallback_model": cls.FALLBACK_LLM_MODEL,
            "max_tokens": cls.MAX_TOKENS,
            "temperature": cls.TEMPERATURE,
            "use_gpu": use_gpu
        }
    
    @classmethod
    def get_agent_config(cls) -> Dict[str, Any]:
        """Get agent configuration"""
        return {
            "memory_size": cls.AGENT_MEMORY_SIZE,
            "auto_routing": cls.ENABLE_AUTO_ROUTING,
            "confidence_threshold": cls.ROUTING_CONFIDENCE_THRESHOLD,
            "max_concurrent": cls.MAX_CONCURRENT_QUERIES
        }
    
    @classmethod
    def get_rag_config(cls) -> Dict[str, Any]:
        """Get RAG configuration"""
        return {
            "chunk_size": cls.CHUNK_SIZE,
            "chunk_overlap": cls.CHUNK_OVERLAP,
            "max_documents": cls.MAX_DOCUMENTS,
            "similarity_threshold": cls.SIMILARITY_THRESHOLD,
            "embedding_model": cls.EMBEDDING_MODEL
        }
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate configuration settings"""
        errors = []
        
        # Check required directories
        if not cls.UPLOAD_DIR.exists():
            try:
                cls.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                errors.append(f"Cannot create upload directory: {e}")
        
        # Check numeric ranges
        if cls.TEMPERATURE < 0 or cls.TEMPERATURE > 2:
            errors.append("Temperature must be between 0 and 2")
        
        if cls.CHUNK_SIZE < 100 or cls.CHUNK_SIZE > 4000:
            errors.append("Chunk size must be between 100 and 4000")
        
        if cls.SIMILARITY_THRESHOLD < 0 or cls.SIMILARITY_THRESHOLD > 1:
            errors.append("Similarity threshold must be between 0 and 1")
        
        if errors:
            print("Configuration validation errors:")
            for error in errors:
                print(f"  - {error}")
            return False
        
        return True

# Global configuration instance
config = Config()

# Validate configuration on import
if not config.validate_config():
    print("Warning: Configuration validation failed. Some features may not work correctly.")
