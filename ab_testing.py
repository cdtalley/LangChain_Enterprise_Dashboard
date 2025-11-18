"""
A/B Testing Framework
=====================
Enterprise-grade A/B testing system with statistical significance testing.
Demonstrates advanced Python skills in:
- Statistical hypothesis testing
- Experiment design and management
- Traffic splitting and randomization
- Performance analysis
- Early stopping logic
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from scipy import stats
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()


class ExperimentStatus(Enum):
    """Experiment status"""
    DRAFT = "draft"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    STOPPED = "stopped"


class MetricType(Enum):
    """Metric types for analysis"""
    CONTINUOUS = "continuous"  # e.g., response time, revenue
    BINARY = "binary"  # e.g., conversion, click
    COUNT = "count"  # e.g., page views, events


@dataclass
class ExperimentConfig:
    """A/B test experiment configuration"""
    name: str
    description: str
    hypothesis: str
    metric_name: str
    metric_type: MetricType
    baseline_model: str  # Model name/version
    treatment_model: str  # Model name/version
    traffic_split: float  # Percentage for treatment (0.0-1.0)
    min_sample_size: int
    max_duration_days: int
    significance_level: float = 0.05
    power: float = 0.80
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        data['metric_type'] = self.metric_type.value
        data['created_at'] = self.created_at.isoformat()
        return data


class Experiment(Base):
    """Database model for experiments"""
    __tablename__ = "experiments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    hypothesis = Column(Text)
    metric_name = Column(String)
    metric_type = Column(String)
    baseline_model = Column(String)
    treatment_model = Column(String)
    traffic_split = Column(Float)
    min_sample_size = Column(Integer)
    max_duration_days = Column(Integer)
    significance_level = Column(Float)
    power = Column(Float)
    status = Column(String, default=ExperimentStatus.DRAFT.value)
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    results = Column(JSON)


class ExperimentEvent(Base):
    """Individual experiment events/observations"""
    __tablename__ = "experiment_events"
    
    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(Integer, index=True)
    user_id = Column(String, index=True)
    variant = Column(String)  # "baseline" or "treatment"
    metric_value = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON)


class ABTestingFramework:
    """
    Enterprise A/B Testing Framework
    
    Features:
    - Statistical significance testing (t-test, chi-square, etc.)
    - Traffic splitting and randomization
    - Sample size calculation
    - Early stopping logic
    - Experiment tracking and analysis
    """
    
    def __init__(self, db_url: str = "sqlite:///ab_testing.db"):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        logger.info("A/B Testing Framework initialized")
    
    def create_experiment(self, config: ExperimentConfig) -> int:
        """Create a new A/B test experiment"""
        db = self.SessionLocal()
        try:
            experiment = Experiment(
                name=config.name,
                description=config.description,
                hypothesis=config.hypothesis,
                metric_name=config.metric_name,
                metric_type=config.metric_type.value,
                baseline_model=config.baseline_model,
                treatment_model=config.treatment_model,
                traffic_split=config.traffic_split,
                min_sample_size=config.min_sample_size,
                max_duration_days=config.max_duration_days,
                significance_level=config.significance_level,
                power=config.power,
                status=ExperimentStatus.DRAFT.value
            )
            db.add(experiment)
            db.commit()
            db.refresh(experiment)
            logger.info(f"Experiment '{config.name}' created with ID {experiment.id}")
            return experiment.id
        finally:
            db.close()
    
    def start_experiment(self, experiment_id: int):
        """Start an experiment"""
        db = self.SessionLocal()
        try:
            experiment = db.query(Experiment).filter(Experiment.id == experiment_id).first()
            if not experiment:
                raise ValueError(f"Experiment {experiment_id} not found")
            
            experiment.status = ExperimentStatus.RUNNING.value
            experiment.started_at = datetime.utcnow()
            db.commit()
            logger.info(f"Experiment {experiment_id} started")
        finally:
            db.close()
    
    def assign_variant(self, experiment_id: int, user_id: str) -> str:
        """
        Assign user to baseline or treatment variant
        
        Uses consistent hashing to ensure same user gets same variant
        """
        db = self.SessionLocal()
        try:
            experiment = db.query(Experiment).filter(Experiment.id == experiment_id).first()
            if not experiment or experiment.status != ExperimentStatus.RUNNING.value:
                return "baseline"  # Default to baseline if experiment not running
            
            # Consistent hashing based on user_id and experiment_id
            hash_value = hash(f"{user_id}_{experiment_id}") % 100
            threshold = experiment.traffic_split * 100
            
            variant = "treatment" if hash_value < threshold else "baseline"
            return variant
        finally:
            db.close()
    
    def record_event(
        self,
        experiment_id: int,
        user_id: str,
        metric_value: float,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Record an experiment event"""
        db = self.SessionLocal()
        try:
            variant = self.assign_variant(experiment_id, user_id)
            
            event = ExperimentEvent(
                experiment_id=experiment_id,
                user_id=user_id,
                variant=variant,
                metric_value=metric_value,
                metadata=metadata or {}
            )
            db.add(event)
            db.commit()
        finally:
            db.close()
    
    def analyze_experiment(self, experiment_id: int) -> Dict[str, Any]:
        """
        Analyze experiment results with statistical tests
        
        Returns:
            Dictionary with statistical analysis results
        """
        db = self.SessionLocal()
        try:
            experiment = db.query(Experiment).filter(Experiment.id == experiment_id).first()
            if not experiment:
                raise ValueError(f"Experiment {experiment_id} not found")
            
            # Get all events for this experiment
            events = db.query(ExperimentEvent).filter(
                ExperimentEvent.experiment_id == experiment_id
            ).all()
            
            if len(events) < 100:  # Minimum sample size
                return {
                    'status': 'insufficient_data',
                    'message': f'Only {len(events)} events collected, need at least 100'
                }
            
            # Split by variant
            baseline_values = [e.metric_value for e in events if e.variant == "baseline"]
            treatment_values = [e.metric_value for e in events if e.variant == "treatment"]
            
            if len(baseline_values) == 0 or len(treatment_values) == 0:
                return {
                    'status': 'insufficient_data',
                    'message': 'No data for one or both variants'
                }
            
            # Perform statistical test based on metric type
            metric_type = MetricType(experiment.metric_type)
            
            if metric_type == MetricType.CONTINUOUS:
                results = self._test_continuous(baseline_values, treatment_values, experiment.significance_level)
            elif metric_type == MetricType.BINARY:
                results = self._test_binary(baseline_values, treatment_values, experiment.significance_level)
            else:  # COUNT
                results = self._test_count(baseline_values, treatment_values, experiment.significance_level)
            
            # Calculate effect size
            baseline_mean = np.mean(baseline_values)
            treatment_mean = np.mean(treatment_values)
            relative_lift = ((treatment_mean - baseline_mean) / baseline_mean * 100) if baseline_mean != 0 else 0
            
            # Check if experiment should stop early
            should_stop = self._check_early_stopping(
                baseline_values,
                treatment_values,
                experiment.significance_level,
                experiment.min_sample_size
            )
            
            analysis = {
                'experiment_id': experiment_id,
                'experiment_name': experiment.name,
                'status': 'running',
                'sample_sizes': {
                    'baseline': len(baseline_values),
                    'treatment': len(treatment_values),
                    'total': len(events)
                },
                'metrics': {
                    'baseline': {
                        'mean': float(baseline_mean),
                        'std': float(np.std(baseline_values)),
                        'median': float(np.median(baseline_values))
                    },
                    'treatment': {
                        'mean': float(treatment_mean),
                        'std': float(np.std(treatment_values)),
                        'median': float(np.median(treatment_values))
                    }
                },
                'statistical_test': results,
                'effect_size': {
                    'absolute_difference': float(treatment_mean - baseline_mean),
                    'relative_lift_percent': float(relative_lift)
                },
                'should_stop_early': should_stop,
                'recommendation': self._get_recommendation(results, relative_lift, should_stop)
            }
            
            # Update experiment with results
            experiment.results = analysis
            db.commit()
            
            return analysis
        finally:
            db.close()
    
    def _test_continuous(self, baseline: List[float], treatment: List[float], alpha: float) -> Dict[str, Any]:
        """Perform t-test for continuous metrics"""
        t_stat, p_value = stats.ttest_ind(treatment, baseline)
        
        return {
            'test_name': 'two_sample_t_test',
            'test_statistic': float(t_stat),
            'p_value': float(p_value),
            'is_significant': p_value < alpha,
            'alpha': alpha,
            'interpretation': self._interpret_p_value(p_value, alpha)
        }
    
    def _test_binary(self, baseline: List[float], treatment: List[float], alpha: float) -> Dict[str, Any]:
        """Perform chi-square test for binary metrics"""
        # Convert to binary outcomes
        baseline_success = sum(baseline)
        baseline_total = len(baseline)
        treatment_success = sum(treatment)
        treatment_total = len(treatment)
        
        # Chi-square test
        contingency_table = np.array([
            [baseline_success, baseline_total - baseline_success],
            [treatment_success, treatment_total - treatment_success]
        ])
        
        chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
        
        return {
            'test_name': 'chi_square_test',
            'test_statistic': float(chi2),
            'p_value': float(p_value),
            'degrees_of_freedom': int(dof),
            'is_significant': p_value < alpha,
            'alpha': alpha,
            'conversion_rates': {
                'baseline': baseline_success / baseline_total if baseline_total > 0 else 0,
                'treatment': treatment_success / treatment_total if treatment_total > 0 else 0
            },
            'interpretation': self._interpret_p_value(p_value, alpha)
        }
    
    def _test_count(self, baseline: List[float], treatment: List[float], alpha: float) -> Dict[str, Any]:
        """Perform Mann-Whitney U test for count metrics"""
        u_stat, p_value = stats.mannwhitneyu(treatment, baseline, alternative='two-sided')
        
        return {
            'test_name': 'mann_whitney_u_test',
            'test_statistic': float(u_stat),
            'p_value': float(p_value),
            'is_significant': p_value < alpha,
            'alpha': alpha,
            'interpretation': self._interpret_p_value(p_value, alpha)
        }
    
    def _interpret_p_value(self, p_value: float, alpha: float) -> str:
        """Interpret p-value"""
        if p_value < alpha:
            return f"Statistically significant (p={p_value:.4f} < {alpha})"
        else:
            return f"Not statistically significant (p={p_value:.4f} >= {alpha})"
    
    def _check_early_stopping(
        self,
        baseline: List[float],
        treatment: List[float],
        alpha: float,
        min_sample_size: int
    ) -> bool:
        """Check if experiment should stop early (for futility or success)"""
        if len(baseline) < min_sample_size or len(treatment) < min_sample_size:
            return False
        
        # Check for clear winner with high confidence
        baseline_mean = np.mean(baseline)
        treatment_mean = np.mean(treatment)
        
        # Use sequential testing approach
        t_stat, p_value = stats.ttest_ind(treatment, baseline)
        
        # Stop early if highly significant (p < alpha/2) or clearly futile
        if p_value < alpha / 2:
            return True
        
        # Check for futility (very small effect size)
        effect_size = abs(treatment_mean - baseline_mean) / (np.std(baseline) + 1e-10)
        if effect_size < 0.1:  # Very small effect
            return True
        
        return False
    
    def _get_recommendation(
        self,
        test_results: Dict[str, Any],
        relative_lift: float,
        should_stop: bool
    ) -> str:
        """Get recommendation based on analysis"""
        if should_stop:
            if test_results.get('is_significant', False):
                if relative_lift > 0:
                    return "Stop experiment: Treatment is significantly better. Consider promoting to production."
                else:
                    return "Stop experiment: Baseline is significantly better. Keep baseline."
            else:
                return "Stop experiment: No significant difference detected. Keep baseline."
        else:
            if test_results.get('is_significant', False):
                if relative_lift > 0:
                    return "Continue experiment: Treatment showing promise. Monitor closely."
                else:
                    return "Continue experiment: Baseline performing better. Consider stopping."
            else:
                return "Continue experiment: Need more data to reach statistical significance."
    
    def calculate_sample_size(
        self,
        baseline_rate: float,
        minimum_detectable_effect: float,
        alpha: float = 0.05,
        power: float = 0.80
    ) -> int:
        """
        Calculate required sample size for experiment
        
        Args:
            baseline_rate: Baseline conversion rate or mean
            minimum_detectable_effect: Minimum effect size to detect (as proportion)
            alpha: Significance level
            power: Statistical power
            
        Returns:
            Required sample size per variant
        """
        from scipy.stats import norm
        
        z_alpha = norm.ppf(1 - alpha / 2)
        z_beta = norm.ppf(power)
        
        treatment_rate = baseline_rate * (1 + minimum_detectable_effect)
        
        p_pooled = (baseline_rate + treatment_rate) / 2
        
        numerator = 2 * (z_alpha + z_beta) ** 2 * p_pooled * (1 - p_pooled)
        denominator = (treatment_rate - baseline_rate) ** 2
        
        n = numerator / denominator
        
        return int(np.ceil(n))
    
    def list_experiments(
        self,
        status: Optional[ExperimentStatus] = None
    ) -> List[Dict[str, Any]]:
        """List all experiments"""
        db = self.SessionLocal()
        try:
            query = db.query(Experiment)
            if status:
                query = query.filter(Experiment.status == status.value)
            
            experiments = query.order_by(Experiment.created_at.desc()).all()
            
            return [{
                'id': exp.id,
                'name': exp.name,
                'status': exp.status,
                'metric_name': exp.metric_name,
                'baseline_model': exp.baseline_model,
                'treatment_model': exp.treatment_model,
                'created_at': exp.created_at.isoformat(),
                'started_at': exp.started_at.isoformat() if exp.started_at else None,
                'has_results': exp.results is not None
            } for exp in experiments]
        finally:
            db.close()
    
    def get_experiment_summary(self, experiment_id: int) -> Dict[str, Any]:
        """Get comprehensive experiment summary"""
        db = self.SessionLocal()
        try:
            experiment = db.query(Experiment).filter(Experiment.id == experiment_id).first()
            if not experiment:
                raise ValueError(f"Experiment {experiment_id} not found")
            
            # Get event counts
            events = db.query(ExperimentEvent).filter(
                ExperimentEvent.experiment_id == experiment_id
            ).all()
            
            baseline_count = sum(1 for e in events if e.variant == "baseline")
            treatment_count = sum(1 for e in events if e.variant == "treatment")
            
            summary = {
                'experiment': {
                    'id': experiment.id,
                    'name': experiment.name,
                    'description': experiment.description,
                    'hypothesis': experiment.hypothesis,
                    'status': experiment.status,
                    'metric_name': experiment.metric_name,
                    'metric_type': experiment.metric_type,
                    'baseline_model': experiment.baseline_model,
                    'treatment_model': experiment.treatment_model,
                    'traffic_split': experiment.traffic_split,
                    'created_at': experiment.created_at.isoformat(),
                    'started_at': experiment.started_at.isoformat() if experiment.started_at else None
                },
                'statistics': {
                    'total_events': len(events),
                    'baseline_events': baseline_count,
                    'treatment_events': treatment_count,
                    'progress_percent': min(100, (len(events) / experiment.min_sample_size * 100))
                },
                'results': experiment.results
            }
            
            return summary
        finally:
            db.close()

