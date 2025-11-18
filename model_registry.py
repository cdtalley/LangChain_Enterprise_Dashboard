"""
Model Registry & Management System
===================================
Enterprise-grade model versioning, tracking, and lifecycle management.
Demonstrates advanced Python skills in:
- Model serialization and versioning
- Metadata management
- Performance tracking
- Model serving integration
"""

import os
import json
import pickle
import hashlib
import shutil
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import joblib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()


class ModelStage(Enum):
    """Model lifecycle stages"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    ARCHIVED = "archived"


class ModelType(Enum):
    """Supported model types"""
    LLM = "llm"
    EMBEDDING = "embedding"
    CLASSIFIER = "classifier"
    REGRESSOR = "regressor"
    RAG = "rag"
    AGENT = "agent"


@dataclass
class ModelMetadata:
    """Comprehensive model metadata"""
    name: str
    version: str
    model_type: str
    stage: str
    description: str
    author: str
    created_at: datetime
    updated_at: datetime
    performance_metrics: Dict[str, float]
    hyperparameters: Dict[str, Any]
    training_data_hash: Optional[str] = None
    model_size_mb: Optional[float] = None
    dependencies: Optional[Dict[str, str]] = None
    tags: Optional[List[str]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ModelMetadata':
        """Create from dictionary"""
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        return cls(**data)


class ModelRegistry(Base):
    """Database model for model registry"""
    __tablename__ = "model_registry"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    version = Column(String, index=True)
    model_type = Column(String)
    stage = Column(String, index=True)
    description = Column(Text)
    author = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    performance_metrics = Column(JSON)
    hyperparameters = Column(JSON)
    training_data_hash = Column(String)
    model_size_mb = Column(Float)
    dependencies = Column(JSON)
    tags = Column(JSON)
    model_path = Column(String)
    is_active = Column(Boolean, default=True)


class ModelRegistryManager:
    """
    Enterprise Model Registry Manager
    
    Features:
    - Model versioning and tracking
    - Performance metrics storage
    - Model lifecycle management
    - Model serving integration
    - Metadata search and filtering
    """
    
    def __init__(self, registry_path: str = "./models/registry", db_url: str = "sqlite:///model_registry.db"):
        self.registry_path = Path(registry_path)
        self.registry_path.mkdir(parents=True, exist_ok=True)
        
        # Database setup
        self.engine = create_engine(db_url)
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        logger.info(f"Model Registry initialized at {self.registry_path}")
    
    def register_model(
        self,
        model: Any,
        name: str,
        version: str,
        model_type: ModelType,
        description: str,
        author: str,
        performance_metrics: Dict[str, float],
        hyperparameters: Dict[str, Any],
        stage: ModelStage = ModelStage.DEVELOPMENT,
        training_data_hash: Optional[str] = None,
        dependencies: Optional[Dict[str, str]] = None,
        tags: Optional[List[str]] = None
    ) -> str:
        """
        Register a new model version
        
        Args:
            model: The model object to register
            name: Model name
            version: Model version (e.g., "1.0.0")
            model_type: Type of model
            description: Model description
            author: Author name
            performance_metrics: Dictionary of performance metrics
            hyperparameters: Model hyperparameters
            stage: Model lifecycle stage
            training_data_hash: Hash of training data (optional)
            dependencies: Python dependencies (optional)
            tags: List of tags (optional)
            
        Returns:
            Model ID
        """
        try:
            # Create model directory
            model_dir = self.registry_path / name / version
            model_dir.mkdir(parents=True, exist_ok=True)
            
            # Save model
            model_path = model_dir / "model.pkl"
            self._save_model(model, model_path)
            
            # Calculate model size
            model_size_mb = model_path.stat().st_size / (1024 * 1024)
            
            # Create metadata
            metadata = ModelMetadata(
                name=name,
                version=version,
                model_type=model_type.value,
                stage=stage.value,
                description=description,
                author=author,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                performance_metrics=performance_metrics,
                hyperparameters=hyperparameters,
                training_data_hash=training_data_hash,
                model_size_mb=model_size_mb,
                dependencies=dependencies or {},
                tags=tags or []
            )
            
            # Save metadata
            metadata_path = model_dir / "metadata.json"
            with open(metadata_path, 'w') as f:
                json.dump(metadata.to_dict(), f, indent=2)
            
            # Store in database
            db = self.SessionLocal()
            try:
                registry_entry = ModelRegistry(
                    name=name,
                    version=version,
                    model_type=model_type.value,
                    stage=stage.value,
                    description=description,
                    author=author,
                    performance_metrics=performance_metrics,
                    hyperparameters=hyperparameters,
                    training_data_hash=training_data_hash,
                    model_size_mb=model_size_mb,
                    dependencies=dependencies or {},
                    tags=tags or [],
                    model_path=str(model_path)
                )
                db.add(registry_entry)
                db.commit()
                model_id = registry_entry.id
                logger.info(f"Model {name} v{version} registered with ID {model_id}")
                return str(model_id)
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"Failed to register model: {e}", exc_info=True)
            raise
    
    def _save_model(self, model: Any, path: Path):
        """Save model using appropriate serialization method"""
        try:
            # Try joblib first (better for scikit-learn models)
            if hasattr(model, 'predict') or hasattr(model, 'transform'):
                joblib.dump(model, path)
            else:
                # Fallback to pickle
                with open(path, 'wb') as f:
                    pickle.dump(model, f)
        except Exception as e:
            logger.warning(f"Joblib failed, using pickle: {e}")
            with open(path, 'wb') as f:
                pickle.dump(model, f)
    
    def load_model(self, name: str, version: Optional[str] = None, stage: Optional[ModelStage] = None) -> Tuple[Any, ModelMetadata]:
        """
        Load a model by name, version, or stage
        
        Args:
            name: Model name
            version: Specific version (if None, loads latest)
            stage: Stage (if None, uses version or latest)
            
        Returns:
            Tuple of (model, metadata)
        """
        db = self.SessionLocal()
        try:
            query = db.query(ModelRegistry).filter(ModelRegistry.name == name, ModelRegistry.is_active == True)
            
            if version:
                query = query.filter(ModelRegistry.version == version)
            elif stage:
                query = query.filter(ModelRegistry.stage == stage.value)
            else:
                # Get latest version
                query = query.order_by(ModelRegistry.created_at.desc())
            
            registry_entry = query.first()
            
            if not registry_entry:
                raise ValueError(f"Model {name} not found")
            
            # Load model
            model_path = Path(registry_entry.model_path)
            model = self._load_model(model_path)
            
            # Load metadata
            metadata_path = model_path.parent / "metadata.json"
            with open(metadata_path, 'r') as f:
                metadata_dict = json.load(f)
            metadata = ModelMetadata.from_dict(metadata_dict)
            
            return model, metadata
            
        finally:
            db.close()
    
    def _load_model(self, path: Path) -> Any:
        """Load model from file"""
        if not path.exists():
            raise FileNotFoundError(f"Model file not found: {path}")
        
        try:
            return joblib.load(path)
        except (joblib.exceptions.UnpicklingError, EOFError, ValueError) as e:
            logger.warning(f"Joblib load failed, trying pickle: {e}")
            try:
                with open(path, 'rb') as f:
                    return pickle.load(f)
            except (pickle.UnpicklingError, EOFError, ValueError) as e2:
                raise ValueError(f"Failed to load model from {path}: {e2}") from e2
        except Exception as e:
            raise ValueError(f"Unexpected error loading model from {path}: {e}") from e
    
    def list_models(
        self,
        name: Optional[str] = None,
        model_type: Optional[ModelType] = None,
        stage: Optional[ModelStage] = None,
        tags: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """List models with optional filtering"""
        db = self.SessionLocal()
        try:
            query = db.query(ModelRegistry).filter(ModelRegistry.is_active == True)
            
            if name:
                query = query.filter(ModelRegistry.name == name)
            if model_type:
                query = query.filter(ModelRegistry.model_type == model_type.value)
            if stage:
                query = query.filter(ModelRegistry.stage == stage.value)
            if tags:
                for tag in tags:
                    query = query.filter(ModelRegistry.tags.contains([tag]))
            
            results = query.order_by(ModelRegistry.created_at.desc()).all()
            
            return [self._registry_to_dict(r) for r in results]
        finally:
            db.close()
    
    def _registry_to_dict(self, registry_entry: ModelRegistry) -> Dict[str, Any]:
        """Convert registry entry to dictionary"""
        return {
            'id': registry_entry.id,
            'name': registry_entry.name,
            'version': registry_entry.version,
            'model_type': registry_entry.model_type,
            'stage': registry_entry.stage,
            'description': registry_entry.description,
            'author': registry_entry.author,
            'created_at': registry_entry.created_at.isoformat(),
            'updated_at': registry_entry.updated_at.isoformat(),
            'performance_metrics': registry_entry.performance_metrics,
            'hyperparameters': registry_entry.hyperparameters,
            'model_size_mb': registry_entry.model_size_mb,
            'tags': registry_entry.tags
        }
    
    def promote_model(self, name: str, version: str, target_stage: ModelStage):
        """Promote model to a new stage (e.g., staging -> production)"""
        db = self.SessionLocal()
        try:
            model = db.query(ModelRegistry).filter(
                ModelRegistry.name == name,
                ModelRegistry.version == version
            ).first()
            
            if not model:
                raise ValueError(f"Model {name} v{version} not found")
            
            model.stage = target_stage.value
            model.updated_at = datetime.utcnow()
            db.commit()
            
            logger.info(f"Model {name} v{version} promoted to {target_stage.value}")
        finally:
            db.close()
    
    def get_model_performance_history(self, name: str) -> pd.DataFrame:
        """Get performance metrics history for a model"""
        db = self.SessionLocal()
        try:
            models = db.query(ModelRegistry).filter(
                ModelRegistry.name == name,
                ModelRegistry.is_active == True
            ).order_by(ModelRegistry.created_at).all()
            
            records = []
            for model in models:
                metrics = model.performance_metrics or {}
                record = {
                    'version': model.version,
                    'stage': model.stage,
                    'created_at': model.created_at,
                    **metrics
                }
                records.append(record)
            
            return pd.DataFrame(records)
        finally:
            db.close()
    
    def compare_models(self, name: str, version1: str, version2: str) -> Dict[str, Any]:
        """Compare two model versions"""
        db = self.SessionLocal()
        try:
            model1 = db.query(ModelRegistry).filter(
                ModelRegistry.name == name,
                ModelRegistry.version == version1
            ).first()
            
            model2 = db.query(ModelRegistry).filter(
                ModelRegistry.name == name,
                ModelRegistry.version == version2
            ).first()
            
            if not model1 or not model2:
                raise ValueError("One or both models not found")
            
            comparison = {
                'model1': {
                    'version': model1.version,
                    'stage': model1.stage,
                    'metrics': model1.performance_metrics,
                    'created_at': model1.created_at.isoformat()
                },
                'model2': {
                    'version': model2.version,
                    'stage': model2.stage,
                    'metrics': model2.performance_metrics,
                    'created_at': model2.created_at.isoformat()
                },
                'differences': {}
            }
            
            # Compare metrics
            metrics1 = model1.performance_metrics or {}
            metrics2 = model2.performance_metrics or {}
            
            all_metrics = set(metrics1.keys()) | set(metrics2.keys())
            for metric in all_metrics:
                val1 = metrics1.get(metric, None)
                val2 = metrics2.get(metric, None)
                if val1 is not None and val2 is not None:
                    diff = val2 - val1
                    pct_change = (diff / val1 * 100) if val1 != 0 else 0
                    comparison['differences'][metric] = {
                        'v1': val1,
                        'v2': val2,
                        'absolute_change': diff,
                        'percent_change': pct_change
                    }
            
            return comparison
        finally:
            db.close()
    
    def archive_model(self, name: str, version: str):
        """Archive a model version"""
        db = self.SessionLocal()
        try:
            model = db.query(ModelRegistry).filter(
                ModelRegistry.name == name,
                ModelRegistry.version == version
            ).first()
            
            if not model:
                raise ValueError(f"Model {name} v{version} not found")
            
            model.stage = ModelStage.ARCHIVED.value
            model.is_active = False
            model.updated_at = datetime.utcnow()
            db.commit()
            
            logger.info(f"Model {name} v{version} archived")
        finally:
            db.close()

