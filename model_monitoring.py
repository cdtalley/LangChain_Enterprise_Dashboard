"""
Model Performance Monitoring & Drift Detection
==============================================
Enterprise-grade model monitoring with drift detection.
Demonstrates advanced Python skills in:
- Statistical process control
- Data drift detection
- Performance degradation monitoring
- Alerting and anomaly detection
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import logging
from scipy import stats
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()


class DriftType(Enum):
    """Types of drift"""
    DATA_DRIFT = "data_drift"
    CONCEPT_DRIFT = "concept_drift"
    PERFORMANCE_DEGRADATION = "performance_degradation"


class AlertSeverity(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class DriftAlert:
    """Drift detection alert"""
    model_name: str
    drift_type: DriftType
    severity: AlertSeverity
    metric_name: str
    baseline_value: float
    current_value: float
    drift_score: float
    timestamp: datetime
    message: str


class ModelPerformance(Base):
    """Database model for model performance metrics"""
    __tablename__ = "model_performance"
    
    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, index=True)
    model_version = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    metric_name = Column(String, index=True)
    metric_value = Column(Float)
    prediction_count = Column(Integer)
    metadata = Column(JSON)


class ModelMonitoring:
    """
    Model Performance Monitoring System
    
    Features:
    - Real-time performance tracking
    - Data drift detection (KS test, PSI)
    - Concept drift detection
    - Performance degradation alerts
    - Statistical process control charts
    """
    
    def __init__(self, db_url: str = "sqlite:///model_monitoring.db"):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        logger.info("Model Monitoring System initialized")
    
    def log_performance(
        self,
        model_name: str,
        model_version: str,
        metric_name: str,
        metric_value: float,
        prediction_count: int = 1,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Log model performance metrics"""
        db = self.SessionLocal()
        try:
            performance = ModelPerformance(
                model_name=model_name,
                model_version=model_version,
                metric_name=metric_name,
                metric_value=metric_value,
                prediction_count=prediction_count,
                metadata=metadata or {}
            )
            db.add(performance)
            db.commit()
        finally:
            db.close()
    
    def detect_data_drift(
        self,
        model_name: str,
        baseline_data: np.ndarray,
        current_data: np.ndarray,
        feature_name: str
    ) -> Dict[str, Any]:
        """
        Detect data drift using Kolmogorov-Smirnov test
        
        Returns drift score and significance
        """
        if len(baseline_data) == 0 or len(current_data) == 0:
            return {
                'drift_detected': False,
                'drift_score': 0.0,
                'message': 'Insufficient data for drift detection'
            }
        
        # Kolmogorov-Smirnov test
        ks_statistic, p_value = stats.ks_2samp(baseline_data, current_data)
        
        # Population Stability Index (PSI)
        psi = self._calculate_psi(baseline_data, current_data)
        
        # Drift score (0-1, higher = more drift)
        drift_score = max(ks_statistic, psi / 10.0)  # Normalize PSI
        
        drift_detected = p_value < 0.05 or psi > 0.2
        
        return {
            'drift_detected': drift_detected,
            'drift_score': float(drift_score),
            'ks_statistic': float(ks_statistic),
            'ks_p_value': float(p_value),
            'psi': float(psi),
            'baseline_mean': float(np.mean(baseline_data)),
            'current_mean': float(np.mean(current_data)),
            'baseline_std': float(np.std(baseline_data)),
            'current_std': float(np.std(current_data)),
            'feature_name': feature_name,
            'severity': self._determine_severity(drift_score, psi)
        }
    
    def _calculate_psi(self, baseline: np.ndarray, current: np.ndarray, bins: int = 10) -> float:
        """Calculate Population Stability Index"""
        # Create bins based on baseline distribution
        _, bin_edges = np.histogram(baseline, bins=bins)
        
        # Calculate expected (baseline) and actual (current) distributions
        baseline_hist, _ = np.histogram(baseline, bins=bin_edges)
        current_hist, _ = np.histogram(current, bins=bin_edges)
        
        # Normalize to probabilities
        baseline_prob = baseline_hist / len(baseline)
        current_prob = current_hist / len(current)
        
        # Avoid division by zero
        baseline_prob = np.where(baseline_prob == 0, 0.0001, baseline_prob)
        current_prob = np.where(current_prob == 0, 0.0001, current_prob)
        
        # Calculate PSI
        psi = np.sum((current_prob - baseline_prob) * np.log(current_prob / baseline_prob))
        
        return psi
    
    def detect_performance_drift(
        self,
        model_name: str,
        model_version: str,
        metric_name: str,
        lookback_days: int = 7,
        threshold_std: float = 2.0
    ) -> Dict[str, Any]:
        """
        Detect performance degradation using statistical process control
        
        Uses control charts to detect anomalies
        """
        db = self.SessionLocal()
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=lookback_days)
            
            # Get recent performance metrics
            recent_metrics = db.query(ModelPerformance).filter(
                ModelPerformance.model_name == model_name,
                ModelPerformance.model_version == model_version,
                ModelPerformance.metric_name == metric_name,
                ModelPerformance.timestamp >= cutoff_date
            ).order_by(ModelPerformance.timestamp).all()
            
            if len(recent_metrics) < 10:
                return {
                    'drift_detected': False,
                    'message': f'Insufficient data points ({len(recent_metrics)} < 10)'
                }
            
            values = np.array([m.metric_value for m in recent_metrics])
            
            # Calculate control limits (3-sigma rule)
            mean = np.mean(values)
            std = np.std(values)
            
            upper_limit = mean + threshold_std * std
            lower_limit = mean - threshold_std * std
            
            # Check for violations
            violations = np.sum((values > upper_limit) | (values < lower_limit))
            violation_rate = violations / len(values)
            
            # Trend detection (using linear regression)
            x = np.arange(len(values))
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, values)
            
            # Determine if there's a significant trend
            trend_detected = p_value < 0.05
            is_degrading = trend_detected and slope < 0
            
            drift_detected = violation_rate > 0.1 or (trend_detected and abs(slope) > std * 0.5)
            
            return {
                'drift_detected': drift_detected,
                'violation_rate': float(violation_rate),
                'mean': float(mean),
                'std': float(std),
                'upper_limit': float(upper_limit),
                'lower_limit': float(lower_limit),
                'trend_detected': trend_detected,
                'trend_slope': float(slope),
                'is_degrading': is_degrading,
                'severity': self._determine_performance_severity(violation_rate, is_degrading),
                'data_points': len(values)
            }
        finally:
            db.close()
    
    def _determine_severity(self, drift_score: float, psi: float) -> str:
        """Determine alert severity based on drift metrics"""
        if psi > 0.5 or drift_score > 0.5:
            return "critical"
        elif psi > 0.25 or drift_score > 0.3:
            return "warning"
        else:
            return "info"
    
    def _determine_performance_severity(self, violation_rate: float, is_degrading: bool) -> str:
        """Determine severity for performance drift"""
        if violation_rate > 0.3 or (is_degrading and violation_rate > 0.15):
            return "critical"
        elif violation_rate > 0.15 or is_degrading:
            return "warning"
        else:
            return "info"
    
    def get_performance_trends(
        self,
        model_name: str,
        model_version: str,
        metric_name: str,
        days: int = 30
    ) -> pd.DataFrame:
        """Get performance trends over time"""
        db = self.SessionLocal()
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            metrics = db.query(ModelPerformance).filter(
                ModelPerformance.model_name == model_name,
                ModelPerformance.model_version == model_version,
                ModelPerformance.metric_name == metric_name,
                ModelPerformance.timestamp >= cutoff_date
            ).order_by(ModelPerformance.timestamp).all()
            
            data = [{
                'timestamp': m.timestamp,
                'metric_value': m.metric_value,
                'prediction_count': m.prediction_count
            } for m in metrics]
            
            return pd.DataFrame(data)
        finally:
            db.close()
    
    def generate_monitoring_report(
        self,
        model_name: str,
        model_version: str,
        days: int = 7
    ) -> Dict[str, Any]:
        """Generate comprehensive monitoring report"""
        db = self.SessionLocal()
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            # Get all metrics for this model
            metrics = db.query(ModelPerformance).filter(
                ModelPerformance.model_name == model_name,
                ModelPerformance.model_version == model_version,
                ModelPerformance.timestamp >= cutoff_date
            ).all()
            
            if not metrics:
                return {'error': 'No metrics found'}
            
            # Group by metric name
            metric_groups = {}
            for m in metrics:
                if m.metric_name not in metric_groups:
                    metric_groups[m.metric_name] = []
                metric_groups[m.metric_name].append(m.metric_value)
            
            report = {
                'model_name': model_name,
                'model_version': model_version,
                'report_period_days': days,
                'total_predictions': sum(m.prediction_count for m in metrics),
                'metrics': {}
            }
            
            for metric_name, values in metric_groups.items():
                values_array = np.array(values)
                
                # Detect drift for this metric
                drift_info = self.detect_performance_drift(
                    model_name, model_version, metric_name, days=days
                )
                
                report['metrics'][metric_name] = {
                    'mean': float(np.mean(values_array)),
                    'std': float(np.std(values_array)),
                    'min': float(np.min(values_array)),
                    'max': float(np.max(values_array)),
                    'p25': float(np.percentile(values_array, 25)),
                    'p50': float(np.percentile(values_array, 50)),
                    'p75': float(np.percentile(values_array, 75)),
                    'p95': float(np.percentile(values_array, 95)),
                    'data_points': len(values_array),
                    'drift_detected': drift_info.get('drift_detected', False),
                    'drift_severity': drift_info.get('severity', 'info')
                }
            
            return report
        finally:
            db.close()

