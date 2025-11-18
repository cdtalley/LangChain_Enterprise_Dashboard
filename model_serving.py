"""
Model Serving API
=================
Production-ready model serving with FastAPI.
Demonstrates MLOps skills in:
- Model serving endpoints
- Batch and real-time inference
- Model versioning in production
- Request/response validation
- Performance monitoring
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import numpy as np
import pandas as pd
import logging
import time
from datetime import datetime
from model_registry import ModelRegistryManager, ModelStage
from model_monitoring import ModelMonitoring

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PredictionRequest(BaseModel):
    """Single prediction request"""
    features: Dict[str, Any] = Field(..., description="Feature dictionary")
    model_name: Optional[str] = Field(None, description="Specific model name")
    model_version: Optional[str] = Field(None, description="Specific model version")
    return_probabilities: bool = Field(False, description="Return class probabilities")


class BatchPredictionRequest(BaseModel):
    """Batch prediction request"""
    instances: List[Dict[str, Any]] = Field(..., description="List of feature dictionaries")
    model_name: Optional[str] = None
    model_version: Optional[str] = None
    return_probabilities: bool = False


class PredictionResponse(BaseModel):
    """Prediction response"""
    prediction: Any
    model_name: str
    model_version: str
    probabilities: Optional[Dict[str, float]] = None
    inference_time_ms: float
    timestamp: str


class BatchPredictionResponse(BaseModel):
    """Batch prediction response"""
    predictions: List[Any]
    probabilities: Optional[List[Dict[str, float]]] = None
    model_name: str
    model_version: str
    total_inference_time_ms: float
    avg_inference_time_ms: float
    timestamp: str


class ModelServingAPI:
    """
    Production Model Serving API
    
    Features:
    - Real-time inference
    - Batch inference
    - Model versioning
    - Performance monitoring
    - Request validation
    """
    
    def __init__(self, registry: ModelRegistryManager, monitoring: ModelMonitoring):
        self.registry = registry
        self.monitoring = monitoring
        self.loaded_models: Dict[str, Any] = {}
        self.model_metadata: Dict[str, Dict] = {}
        
        logger.info("Model Serving API initialized")
    
    def load_model(self, model_name: str, version: Optional[str] = None) -> tuple:
        """Load model into memory (with caching)"""
        cache_key = f"{model_name}:{version or 'latest'}"
        
        if cache_key in self.loaded_models:
            return self.loaded_models[cache_key], self.model_metadata[cache_key]
        
        try:
            model, metadata = self.registry.load_model(
                model_name,
                version=version,
                stage=ModelStage.PRODUCTION if not version else None
            )
            
            self.loaded_models[cache_key] = model
            self.model_metadata[cache_key] = metadata.to_dict()
            
            logger.info(f"Model {model_name} v{metadata.version} loaded")
            return model, metadata.to_dict()
            
        except Exception as e:
            logger.error(f"Failed to load model {model_name}: {e}")
            raise
    
    def predict_single(
        self,
        features: Dict[str, Any],
        model_name: Optional[str] = None,
        model_version: Optional[str] = None,
        return_probabilities: bool = False
    ) -> PredictionResponse:
        """Make single prediction"""
        start_time = time.time()
        
        try:
            # Load model
            model, metadata = self.load_model(model_name or "default-model", model_version)
            
            # Convert features to model input format
            feature_vector = self._prepare_features(features, metadata)
            
            # Make prediction
            prediction = model.predict(feature_vector)
            
            # Get probabilities if requested
            probabilities = None
            if return_probabilities and hasattr(model, 'predict_proba'):
                proba = model.predict_proba(feature_vector)[0]
                class_names = getattr(model, 'classes_', [f"class_{i}" for i in range(len(proba))])
                probabilities = {str(name): float(prob) for name, prob in zip(class_names, proba)}
            
            inference_time = (time.time() - start_time) * 1000
            
            # Log performance
            self.monitoring.log_performance(
                metadata['name'],
                metadata['version'],
                "inference_time_ms",
                inference_time,
                prediction_count=1
            )
            
            return PredictionResponse(
                prediction=float(prediction[0]) if isinstance(prediction, np.ndarray) else prediction,
                model_name=metadata['name'],
                model_version=metadata['version'],
                probabilities=probabilities,
                inference_time_ms=inference_time,
                timestamp=datetime.utcnow().isoformat()
            )
            
        except Exception as e:
            logger.error(f"Prediction failed: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
    
    def predict_batch(
        self,
        instances: List[Dict[str, Any]],
        model_name: Optional[str] = None,
        model_version: Optional[str] = None,
        return_probabilities: bool = False
    ) -> BatchPredictionResponse:
        """Make batch predictions"""
        start_time = time.time()
        
        try:
            # Load model
            model, metadata = self.load_model(model_name or "default-model", model_version)
            
            # Prepare batch features
            feature_matrix = np.array([
                self._prepare_features(instance, metadata)[0]
                for instance in instances
            ])
            
            # Batch prediction
            predictions = model.predict(feature_matrix)
            
            # Get probabilities if requested
            probabilities_list = None
            if return_probabilities and hasattr(model, 'predict_proba'):
                proba_matrix = model.predict_proba(feature_matrix)
                class_names = getattr(model, 'classes_', [f"class_{i}" for i in range(proba_matrix.shape[1])])
                probabilities_list = [
                    {str(name): float(prob) for name, prob in zip(class_names, proba)}
                    for proba in proba_matrix
                ]
            
            total_time = (time.time() - start_time) * 1000
            avg_time = total_time / len(instances)
            
            # Log performance
            self.monitoring.log_performance(
                metadata['name'],
                metadata['version'],
                "batch_inference_time_ms",
                avg_time,
                prediction_count=len(instances)
            )
            
            return BatchPredictionResponse(
                predictions=[float(p) if isinstance(p, np.ndarray) else p for p in predictions],
                probabilities=probabilities_list,
                model_name=metadata['name'],
                model_version=metadata['version'],
                total_inference_time_ms=total_time,
                avg_inference_time_ms=avg_time,
                timestamp=datetime.utcnow().isoformat()
            )
            
        except Exception as e:
            logger.error(f"Batch prediction failed: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Batch prediction failed: {str(e)}")
    
    def _prepare_features(self, features: Dict[str, Any], metadata: Dict) -> np.ndarray:
        """Prepare features for model input"""
        # In production, this would use feature store or transformation pipeline
        # For demo, convert dict to array
        feature_list = list(features.values())
        return np.array([feature_list])
    
    def get_model_info(self, model_name: str, version: Optional[str] = None) -> Dict[str, Any]:
        """Get model information"""
        try:
            model, metadata = self.load_model(model_name, version)
            return {
                "name": metadata['name'],
                "version": metadata['version'],
                "stage": metadata['stage'],
                "performance_metrics": metadata['performance_metrics'],
                "hyperparameters": metadata['hyperparameters'],
                "created_at": metadata['created_at'],
                "is_loaded": True
            }
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Model not found: {str(e)}")
    
    def list_available_models(self) -> List[Dict[str, Any]]:
        """List all available models"""
        models = self.registry.list_models(stage=ModelStage.PRODUCTION)
        return [
            {
                "name": m['name'],
                "version": m['version'],
                "stage": m['stage'],
                "performance_metrics": m['performance_metrics']
            }
            for m in models
        ]


# FastAPI app integration
def create_model_serving_app(registry: ModelRegistryManager, monitoring: ModelMonitoring) -> FastAPI:
    """Create FastAPI app for model serving"""
    app = FastAPI(
        title="Model Serving API",
        description="Production-ready model serving endpoints",
        version="1.0.0"
    )
    
    serving_api = ModelServingAPI(registry, monitoring)
    
    @app.post("/predict", response_model=PredictionResponse)
    async def predict(request: PredictionRequest):
        """Single prediction endpoint"""
        return serving_api.predict_single(
            request.features,
            request.model_name,
            request.model_version,
            request.return_probabilities
        )
    
    @app.post("/predict/batch", response_model=BatchPredictionResponse)
    async def predict_batch(request: BatchPredictionRequest):
        """Batch prediction endpoint"""
        return serving_api.predict_batch(
            request.instances,
            request.model_name,
            request.model_version,
            request.return_probabilities
        )
    
    @app.get("/models")
    async def list_models():
        """List available models"""
        return {"models": serving_api.list_available_models()}
    
    @app.get("/models/{model_name}")
    async def get_model_info(model_name: str, version: Optional[str] = None):
        """Get model information"""
        return serving_api.get_model_info(model_name, version)
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "loaded_models": len(serving_api.loaded_models),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    return app

