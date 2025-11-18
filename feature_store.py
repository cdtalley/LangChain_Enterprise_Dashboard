"""
Feature Store
=============
Production-ready feature store for MLOps.
Demonstrates MLOps skills in:
- Feature versioning and management
- Online and offline feature serving
- Feature transformation pipelines
- Feature monitoring and validation
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import hashlib
import json
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()


class FeatureType(Enum):
    """Feature types"""
    NUMERICAL = "numerical"
    CATEGORICAL = "categorical"
    TEXT = "text"
    EMBEDDING = "embedding"
    TIMESTAMP = "timestamp"


@dataclass
class FeatureDefinition:
    """Feature definition"""
    name: str
    feature_type: FeatureType
    description: str
    transformation: Optional[str] = None  # SQL or Python transformation
    validation_rules: Optional[Dict[str, Any]] = None
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['feature_type'] = self.feature_type.value
        data['created_at'] = self.created_at.isoformat()
        return data


class FeatureSet(Base):
    """Database model for feature sets"""
    __tablename__ = "feature_sets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    version = Column(String, index=True)
    description = Column(Text)
    features = Column(JSON)  # List of feature definitions
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)


class FeatureValue(Base):
    """Database model for feature values (online serving)"""
    __tablename__ = "feature_values"
    
    id = Column(Integer, primary_key=True, index=True)
    feature_set_name = Column(String, index=True)
    entity_id = Column(String, index=True)  # e.g., user_id, product_id
    feature_name = Column(String, index=True)
    feature_value = Column(JSON)  # Can store any type
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    ttl_days = Column(Integer, default=30)  # Time to live


class FeatureStore:
    """
    Production Feature Store
    
    Features:
    - Feature versioning
    - Online feature serving (low latency)
    - Offline feature serving (batch)
    - Feature transformation pipelines
    - Feature validation
    """
    
    def __init__(self, db_url: str = "sqlite:///feature_store.db"):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # In-memory cache for online features
        self.online_cache: Dict[str, Dict[str, Any]] = {}
        
        logger.info("Feature Store initialized")
    
    def create_feature_set(
        self,
        name: str,
        version: str,
        features: List[FeatureDefinition],
        description: str = ""
    ) -> int:
        """Create a new feature set"""
        db = self.SessionLocal()
        try:
            feature_set = FeatureSet(
                name=name,
                version=version,
                description=description,
                features=[f.to_dict() for f in features],
                is_active=True
            )
            db.add(feature_set)
            db.commit()
            db.refresh(feature_set)
            logger.info(f"Feature set {name} v{version} created")
            return feature_set.id
        finally:
            db.close()
    
    def get_feature_set(self, name: str, version: Optional[str] = None) -> Dict[str, Any]:
        """Get feature set definition"""
        db = self.SessionLocal()
        try:
            query = db.query(FeatureSet).filter(FeatureSet.name == name, FeatureSet.is_active == True)
            if version:
                query = query.filter(FeatureSet.version == version)
            else:
                query = query.order_by(FeatureSet.created_at.desc())
            
            feature_set = query.first()
            if not feature_set:
                raise ValueError(f"Feature set {name} not found")
            
            return {
                'id': feature_set.id,
                'name': feature_set.name,
                'version': feature_set.version,
                'description': feature_set.description,
                'features': feature_set.features,
                'created_at': feature_set.created_at.isoformat()
            }
        finally:
            db.close()
    
    def get_online_features(
        self,
        entity_id: str,
        feature_names: List[str],
        feature_set_name: str
    ) -> Dict[str, Any]:
        """
        Get features for online serving (low latency)
        
        Uses cache and database for fast retrieval
        """
        cache_key = f"{feature_set_name}:{entity_id}"
        
        # Check cache first
        if cache_key in self.online_cache:
            cached_features = self.online_cache[cache_key]
            if all(name in cached_features for name in feature_names):
                return {name: cached_features[name] for name in feature_names}
        
        # Query database
        db = self.SessionLocal()
        try:
            feature_values = db.query(FeatureValue).filter(
                FeatureValue.entity_id == entity_id,
                FeatureValue.feature_set_name == feature_set_name,
                FeatureValue.feature_name.in_(feature_names),
                FeatureValue.timestamp >= datetime.utcnow() - timedelta(days=30)
            ).all()
            
            features = {fv.feature_name: fv.feature_value for fv in feature_values}
            
            # Update cache
            self.online_cache[cache_key] = features
            
            return features
        finally:
            db.close()
    
    def get_offline_features(
        self,
        entity_ids: List[str],
        feature_names: List[str],
        feature_set_name: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        Get features for offline/batch serving
        
        Returns pandas DataFrame for batch processing
        """
        db = self.SessionLocal()
        try:
            query = db.query(FeatureValue).filter(
                FeatureValue.entity_id.in_(entity_ids),
                FeatureValue.feature_set_name == feature_set_name,
                FeatureValue.feature_name.in_(feature_names)
            )
            
            if start_date:
                query = query.filter(FeatureValue.timestamp >= start_date)
            if end_date:
                query = query.filter(FeatureValue.timestamp <= end_date)
            
            feature_values = query.all()
            
            # Convert to DataFrame
            data = []
            for fv in feature_values:
                data.append({
                    'entity_id': fv.entity_id,
                    'feature_name': fv.feature_name,
                    'feature_value': fv.feature_value,
                    'timestamp': fv.timestamp
                })
            
            df = pd.DataFrame(data)
            
            if not df.empty:
                # Pivot to wide format
                df_pivot = df.pivot_table(
                    index='entity_id',
                    columns='feature_name',
                    values='feature_value',
                    aggfunc='first'
                )
                return df_pivot
            else:
                return pd.DataFrame()
        finally:
            db.close()
    
    def write_features(
        self,
        feature_set_name: str,
        entity_id: str,
        features: Dict[str, Any],
        ttl_days: int = 30
    ):
        """Write features to store"""
        db = self.SessionLocal()
        try:
            for feature_name, feature_value in features.items():
                feature_value_entry = FeatureValue(
                    feature_set_name=feature_set_name,
                    entity_id=entity_id,
                    feature_name=feature_name,
                    feature_value=feature_value,
                    ttl_days=ttl_days
                )
                db.add(feature_value_entry)
            
            db.commit()
            
            # Update cache
            cache_key = f"{feature_set_name}:{entity_id}"
            if cache_key not in self.online_cache:
                self.online_cache[cache_key] = {}
            self.online_cache[cache_key].update(features)
            
            logger.info(f"Features written for {entity_id} in {feature_set_name}")
        finally:
            db.close()
    
    def validate_features(
        self,
        features: Dict[str, Any],
        feature_set_name: str
    ) -> Tuple[bool, List[str]]:
        """Validate features against feature set definition"""
        feature_set = self.get_feature_set(feature_set_name)
        feature_definitions = feature_set['features']
        
        errors = []
        
        for feat_def in feature_definitions:
            feat_name = feat_def['name']
            feat_type = FeatureType(feat_def['feature_type'])
            
            if feat_name not in features:
                errors.append(f"Missing required feature: {feat_name}")
                continue
            
            value = features[feat_name]
            
            # Type validation
            if feat_type == FeatureType.NUMERICAL:
                if not isinstance(value, (int, float, np.number)):
                    errors.append(f"Feature {feat_name} must be numerical")
            elif feat_type == FeatureType.CATEGORICAL:
                if not isinstance(value, (str, int)):
                    errors.append(f"Feature {feat_name} must be categorical")
            
            # Custom validation rules
            if feat_def.get('validation_rules'):
                rules = feat_def['validation_rules']
                if 'min' in rules and value < rules['min']:
                    errors.append(f"Feature {feat_name} below minimum: {rules['min']}")
                if 'max' in rules and value > rules['max']:
                    errors.append(f"Feature {feat_name} above maximum: {rules['max']}")
                if 'allowed_values' in rules and value not in rules['allowed_values']:
                    errors.append(f"Feature {feat_name} not in allowed values")
        
        return len(errors) == 0, errors
    
    def compute_feature_statistics(self, feature_set_name: str) -> Dict[str, Any]:
        """Compute statistics for features"""
        db = self.SessionLocal()
        try:
            feature_set = self.get_feature_set(feature_set_name)
            feature_names = [f['name'] for f in feature_set['features']]
            
            # Get all feature values
            feature_values = db.query(FeatureValue).filter(
                FeatureValue.feature_set_name == feature_set_name,
                FeatureValue.feature_name.in_(feature_names)
            ).all()
            
            stats = {}
            for feat_name in feature_names:
                values = [
                    fv.feature_value for fv in feature_values
                    if fv.feature_name == feat_name and isinstance(fv.feature_value, (int, float))
                ]
                
                if values:
                    stats[feat_name] = {
                        'count': len(values),
                        'mean': float(np.mean(values)),
                        'std': float(np.std(values)),
                        'min': float(np.min(values)),
                        'max': float(np.max(values)),
                        'p25': float(np.percentile(values, 25)),
                        'p50': float(np.percentile(values, 50)),
                        'p75': float(np.percentile(values, 75))
                    }
            
            return stats
        finally:
            db.close()

