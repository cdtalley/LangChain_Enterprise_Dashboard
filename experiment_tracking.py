"""
Experiment Tracking System
==========================
MLflow-like experiment tracking for model training and evaluation.
Demonstrates advanced Python skills in:
- Experiment logging and versioning
- Metric tracking and visualization
- Parameter tracking
- Artifact management
"""

import os
import json
import pickle
import shutil
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
import logging
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float, JSON
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()


class ExperimentRun(Base):
    """Database model for experiment runs"""
    __tablename__ = "experiment_runs"
    
    id = Column(Integer, primary_key=True, index=True)
    experiment_name = Column(String, index=True)
    run_name = Column(String, index=True)
    status = Column(String)  # running, completed, failed
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    parameters = Column(JSON)
    metrics = Column(JSON)
    tags = Column(JSON)
    artifacts_path = Column(String)
    notes = Column(Text)


class ExperimentTracking:
    """
    Experiment Tracking System (MLflow-like)
    
    Features:
    - Run tracking with parameters and metrics
    - Artifact storage
    - Metric history and visualization
    - Experiment comparison
    """
    
    def __init__(self, tracking_uri: str = "./experiments"):
        self.tracking_uri = Path(tracking_uri)
        self.tracking_uri.mkdir(parents=True, exist_ok=True)
        
        db_url = f"sqlite:///{self.tracking_uri}/experiment_tracking.db"
        self.engine = create_engine(db_url)
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        logger.info(f"Experiment Tracking initialized at {self.tracking_uri}")
    
    def create_experiment(self, experiment_name: str) -> str:
        """Create a new experiment"""
        experiment_dir = self.tracking_uri / experiment_name
        experiment_dir.mkdir(exist_ok=True)
        logger.info(f"Experiment '{experiment_name}' created")
        return str(experiment_dir)
    
    def start_run(
        self,
        experiment_name: str,
        run_name: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None
    ) -> int:
        """Start a new experiment run"""
        if run_name is None:
            run_name = f"run_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        db = self.SessionLocal()
        try:
            run = ExperimentRun(
                experiment_name=experiment_name,
                run_name=run_name,
                status="running",
                parameters={},
                metrics={},
                tags=tags or {},
                artifacts_path=str(self.tracking_uri / experiment_name / run_name)
            )
            db.add(run)
            db.commit()
            db.refresh(run)
            
            # Create artifacts directory
            artifacts_dir = Path(run.artifacts_path)
            artifacts_dir.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"Run '{run_name}' started with ID {run.id}")
            return run.id
        finally:
            db.close()
    
    def log_params(self, run_id: int, params: Dict[str, Any]):
        """Log parameters for a run"""
        db = self.SessionLocal()
        try:
            run = db.query(ExperimentRun).filter(ExperimentRun.id == run_id).first()
            if not run:
                raise ValueError(f"Run {run_id} not found")
            
            # Merge with existing parameters
            existing_params = run.parameters or {}
            existing_params.update(params)
            run.parameters = existing_params
            db.commit()
        finally:
            db.close()
    
    def log_metrics(self, run_id: int, metrics: Dict[str, float], step: Optional[int] = None):
        """Log metrics for a run"""
        db = self.SessionLocal()
        try:
            run = db.query(ExperimentRun).filter(ExperimentRun.id == run_id).first()
            if not run:
                raise ValueError(f"Run {run_id} not found")
            
            # Store metrics with step information
            existing_metrics = run.metrics or {}
            
            for metric_name, metric_value in metrics.items():
                if step is not None:
                    key = f"{metric_name}_step_{step}"
                else:
                    key = metric_name
                
                # Keep history of metrics
                if key not in existing_metrics:
                    existing_metrics[key] = []
                existing_metrics[key].append({
                    'value': float(metric_value),
                    'step': step,
                    'timestamp': datetime.utcnow().isoformat()
                })
            
            run.metrics = existing_metrics
            db.commit()
        finally:
            db.close()
    
    def log_artifact(self, run_id: int, local_path: str, artifact_path: Optional[str] = None):
        """Log an artifact (file) for a run"""
        db = self.SessionLocal()
        try:
            run = db.query(ExperimentRun).filter(ExperimentRun.id == run_id).first()
            if not run:
                raise ValueError(f"Run {run_id} not found")
            
            artifacts_dir = Path(run.artifacts_path)
            
            if artifact_path:
                target_path = artifacts_dir / artifact_path
                target_path.parent.mkdir(parents=True, exist_ok=True)
            else:
                target_path = artifacts_dir / Path(local_path).name
            
            # Copy file
            shutil.copy2(local_path, target_path)
            logger.info(f"Artifact logged: {target_path}")
        finally:
            db.close()
    
    def end_run(self, run_id: int, status: str = "completed", notes: Optional[str] = None):
        """End an experiment run"""
        db = self.SessionLocal()
        try:
            run = db.query(ExperimentRun).filter(ExperimentRun.id == run_id).first()
            if not run:
                raise ValueError(f"Run {run_id} not found")
            
            run.status = status
            run.end_time = datetime.utcnow()
            if notes:
                run.notes = notes
            db.commit()
            logger.info(f"Run {run_id} ended with status '{status}'")
        finally:
            db.close()
    
    def get_run(self, run_id: int) -> Dict[str, Any]:
        """Get run details"""
        db = self.SessionLocal()
        try:
            run = db.query(ExperimentRun).filter(ExperimentRun.id == run_id).first()
            if not run:
                raise ValueError(f"Run {run_id} not found")
            
            return {
                'id': run.id,
                'experiment_name': run.experiment_name,
                'run_name': run.run_name,
                'status': run.status,
                'start_time': run.start_time.isoformat(),
                'end_time': run.end_time.isoformat() if run.end_time else None,
                'parameters': run.parameters,
                'metrics': run.metrics,
                'tags': run.tags,
                'notes': run.notes,
                'duration_seconds': (
                    (run.end_time - run.start_time).total_seconds()
                    if run.end_time else None
                )
            }
        finally:
            db.close()
    
    def search_runs(
        self,
        experiment_name: Optional[str] = None,
        filter_string: Optional[str] = None,
        max_results: int = 100
    ) -> List[Dict[str, Any]]:
        """Search for runs"""
        db = self.SessionLocal()
        try:
            query = db.query(ExperimentRun)
            
            if experiment_name:
                query = query.filter(ExperimentRun.experiment_name == experiment_name)
            
            runs = query.order_by(ExperimentRun.start_time.desc()).limit(max_results).all()
            
            return [self.get_run(run.id) for run in runs]
        finally:
            db.close()
    
    def compare_runs(self, run_ids: List[int]) -> pd.DataFrame:
        """Compare multiple runs"""
        runs_data = []
        
        for run_id in run_ids:
            run = self.get_run(run_id)
            
            # Extract latest metrics
            metrics = run['metrics'] or {}
            latest_metrics = {}
            for metric_name, metric_history in metrics.items():
                if isinstance(metric_history, list) and len(metric_history) > 0:
                    latest_metrics[metric_name] = metric_history[-1]['value']
                elif isinstance(metric_history, (int, float)):
                    latest_metrics[metric_name] = metric_history
            
            run_data = {
                'run_id': run['id'],
                'run_name': run['run_name'],
                'experiment_name': run['experiment_name'],
                'status': run['status'],
                'duration_seconds': run['duration_seconds'],
                **run['parameters'],
                **latest_metrics
            }
            runs_data.append(run_data)
        
        return pd.DataFrame(runs_data)
    
    def get_metric_history(self, experiment_name: str, metric_name: str) -> pd.DataFrame:
        """Get metric history across runs"""
        runs = self.search_runs(experiment_name=experiment_name)
        
        history_data = []
        for run in runs:
            metrics = run['metrics'] or {}
            
            # Find metric in this run
            for key, value in metrics.items():
                if metric_name in key:
                    if isinstance(value, list):
                        for entry in value:
                            history_data.append({
                                'run_id': run['id'],
                                'run_name': run['run_name'],
                                'step': entry.get('step'),
                                'value': entry['value'],
                                'timestamp': entry['timestamp']
                            })
                    elif isinstance(value, (int, float)):
                        history_data.append({
                            'run_id': run['id'],
                            'run_name': run['run_name'],
                            'step': None,
                            'value': value,
                            'timestamp': run['start_time']
                        })
        
        return pd.DataFrame(history_data)

