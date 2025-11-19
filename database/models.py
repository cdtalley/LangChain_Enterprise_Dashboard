"""
Database Models
===============
Centralized SQLAlchemy models for the enterprise workbench.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()


class TimestampMixin:
    """Mixin for timestamp columns."""
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)


class QueryLog(Base, TimestampMixin):
    """Query execution logs."""
    __tablename__ = "query_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    query_text = Column(Text, nullable=False)
    response_text = Column(Text)
    user_id = Column(String(255))
    session_id = Column(String(255))
    execution_time_ms = Column(Float)
    tokens_used = Column(Integer)
    model_used = Column(String(255))
    extra_metadata = Column(JSON, name='metadata')  # Keep DB column name as 'metadata'


class ModelRegistry(Base, TimestampMixin):
    """Model registry entries."""
    __tablename__ = "model_registry"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    version = Column(String(50), nullable=False)
    model_type = Column(String(50), nullable=False)
    stage = Column(String(50), default="development")
    path = Column(String(500), nullable=False)
    description = Column(Text)
    metrics = Column(JSON)
    tags = Column(JSON)
    is_active = Column(Boolean, default=True)
    
    # Note: 'metadata' is reserved in SQLAlchemy, so we use extra_metadata
    # but map it to 'metadata' column in the database


class ExperimentRun(Base, TimestampMixin):
    """Experiment tracking runs."""
    __tablename__ = "experiment_runs"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    experiment_type = Column(String(100))
    status = Column(String(50), default="running")
    parameters = Column(JSON)
    metrics = Column(JSON)
    artifacts = Column(JSON)
    notes = Column(Text)
    started_at = Column(DateTime, default=func.now())
    completed_at = Column(DateTime)


class ModelPerformance(Base, TimestampMixin):
    """Model performance metrics."""
    __tablename__ = "model_performance"
    
    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("model_registry.id"), nullable=False)
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=func.now(), nullable=False, index=True)
    extra_metadata = Column(JSON, name='metadata')  # Keep DB column name as 'metadata'
    
    model = relationship("ModelRegistry", backref="performance_metrics")


class ExperimentEvent(Base, TimestampMixin):
    """A/B testing experiment events."""
    __tablename__ = "experiment_events"
    
    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(String(255), nullable=False, index=True)
    variant = Column(String(100), nullable=False)
    user_id = Column(String(255), index=True)
    event_type = Column(String(100), nullable=False)
    event_value = Column(Float)
    timestamp = Column(DateTime, default=func.now(), nullable=False, index=True)
    extra_metadata = Column(JSON, name='metadata')  # Keep DB column name as 'metadata'

