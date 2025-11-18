"""
Model Retraining Pipeline
=========================
Automated model retraining pipeline for MLOps.
Demonstrates MLOps skills in:
- Automated retraining workflows
- Model versioning
- Performance comparison
- Automated deployment
"""

import logging
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from model_registry import ModelRegistryManager, ModelType, ModelStage
from experiment_tracking import ExperimentTracking
from model_monitoring import ModelMonitoring
from data_validation import DataValidator, DataSchema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RetrainingPipeline:
    """
    Automated Model Retraining Pipeline
    
    Features:
    - Scheduled retraining
    - Performance-based triggers
    - Model comparison
    - Automated promotion
    """
    
    def __init__(
        self,
        registry: ModelRegistryManager,
        tracking: ExperimentTracking,
        monitoring: ModelMonitoring
    ):
        self.registry = registry
        self.tracking = tracking
        self.monitoring = monitoring
        logger.info("Retraining Pipeline initialized")
    
    def train_model(
        self,
        model_name: str,
        training_data: pd.DataFrame,
        target_column: str,
        model_class,
        hyperparameters: Dict[str, Any],
        test_size: float = 0.2,
        validation_size: float = 0.1
    ) -> Dict[str, Any]:
        """
        Train a new model version
        
        Returns training results and model
        """
        logger.info(f"Starting training for {model_name}")
        
        # Prepare data
        X = training_data.drop(columns=[target_column])
        y = training_data[target_column]
        
        # Split data
        X_train, X_temp, y_train, y_temp = train_test_split(
            X, y, test_size=test_size + validation_size, random_state=42
        )
        
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=test_size / (test_size + validation_size), random_state=42
        )
        
        # Start experiment tracking
        run_id = self.tracking.start_run(
            experiment_name=f"{model_name}-training",
            run_name=f"run-{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        )
        
        try:
            # Log hyperparameters
            self.tracking.log_params(run_id, hyperparameters)
            
            # Train model
            model = model_class(**hyperparameters)
            model.fit(X_train, y_train)
            
            # Evaluate on validation set
            y_val_pred = model.predict(X_val)
            val_accuracy = accuracy_score(y_val, y_val_pred)
            val_precision = precision_score(y_val, y_val_pred, average='weighted', zero_division=0)
            val_recall = recall_score(y_val, y_val_pred, average='weighted', zero_division=0)
            val_f1 = f1_score(y_val, y_val_pred, average='weighted', zero_division=0)
            
            # Evaluate on test set
            y_test_pred = model.predict(X_test)
            test_accuracy = accuracy_score(y_test, y_test_pred)
            test_precision = precision_score(y_test, y_test_pred, average='weighted', zero_division=0)
            test_recall = recall_score(y_test, y_test_pred, average='weighted', zero_division=0)
            test_f1 = f1_score(y_test, y_test_pred, average='weighted', zero_division=0)
            
            # Log metrics
            self.tracking.log_metrics(run_id, {
                'val_accuracy': val_accuracy,
                'val_precision': val_precision,
                'val_recall': val_recall,
                'val_f1': val_f1,
                'test_accuracy': test_accuracy,
                'test_precision': test_precision,
                'test_recall': test_recall,
                'test_f1': test_f1
            })
            
            # End run
            self.tracking.end_run(run_id, status="completed")
            
            results = {
                'model': model,
                'run_id': run_id,
                'metrics': {
                    'validation': {
                        'accuracy': val_accuracy,
                        'precision': val_precision,
                        'recall': val_recall,
                        'f1': val_f1
                    },
                    'test': {
                        'accuracy': test_accuracy,
                        'precision': test_precision,
                        'recall': test_recall,
                        'f1': test_f1
                    }
                },
                'training_samples': len(X_train),
                'validation_samples': len(X_val),
                'test_samples': len(X_test)
            }
            
            logger.info(f"Training completed. Test accuracy: {test_accuracy:.4f}")
            return results
            
        except Exception as e:
            self.tracking.end_run(run_id, status="failed", notes=str(e))
            logger.error(f"Training failed: {e}", exc_info=True)
            raise
    
    def should_retrain(
        self,
        model_name: str,
        current_version: str,
        performance_threshold: float = 0.05,
        lookback_days: int = 7
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Determine if model should be retrained
        
        Checks:
        - Performance degradation
        - Data drift
        - Time since last training
        """
        reasons = []
        
        # Check performance degradation
        drift_results = self.monitoring.detect_performance_drift(
            model_name, current_version, "accuracy", lookback_days
        )
        
        if drift_results.get('drift_detected', False):
            if drift_results.get('is_degrading', False):
                reasons.append("Performance degradation detected")
        
        # Check if performance dropped below threshold
        report = self.monitoring.generate_monitoring_report(model_name, current_version, lookback_days)
        if report.get('metrics', {}).get('accuracy', {}).get('mean', 1.0) < performance_threshold:
            reasons.append(f"Performance below threshold: {performance_threshold}")
        
        should_retrain = len(reasons) > 0
        
        return should_retrain, {
            'should_retrain': should_retrain,
            'reasons': reasons,
            'drift_info': drift_results
        }
    
    def compare_and_promote(
        self,
        model_name: str,
        new_version: str,
        baseline_version: str,
        improvement_threshold: float = 0.02
    ) -> Dict[str, Any]:
        """
        Compare new model with baseline and promote if better
        """
        comparison = self.registry.compare_models(model_name, baseline_version, new_version)
        
        # Check if new model is better
        improvements = []
        for metric, diff in comparison.get('differences', {}).items():
            pct_change = diff.get('percent_change', 0)
            if pct_change > improvement_threshold * 100:
                improvements.append({
                    'metric': metric,
                    'improvement': pct_change
                })
        
        should_promote = len(improvements) > 0
        
        if should_promote:
            # Promote to staging
            self.registry.promote_model(model_name, new_version, ModelStage.STAGING)
            logger.info(f"Model {model_name} v{new_version} promoted to staging")
        
        return {
            'should_promote': should_promote,
            'improvements': improvements,
            'comparison': comparison
        }
    
    def automated_retraining_workflow(
        self,
        model_name: str,
        training_data: pd.DataFrame,
        target_column: str,
        model_class,
        hyperparameters: Dict[str, Any],
        current_version: str
    ) -> Dict[str, Any]:
        """
        Complete automated retraining workflow
        
        1. Check if retraining is needed
        2. Train new model
        3. Compare with current model
        4. Promote if better
        """
        logger.info(f"Starting automated retraining workflow for {model_name}")
        
        # Step 1: Check if retraining is needed
        should_retrain, retrain_info = self.should_retrain(model_name, current_version)
        
        if not should_retrain:
            return {
                'retrained': False,
                'reason': 'Retraining not needed',
                'retrain_info': retrain_info
            }
        
        # Step 2: Train new model
        training_results = self.train_model(
            model_name=model_name,
            training_data=training_data,
            target_column=target_column,
            model_class=model_class,
            hyperparameters=hyperparameters
        )
        
        # Generate new version
        version_parts = current_version.split('.')
        new_version = f"{version_parts[0]}.{int(version_parts[1]) + 1}.0"
        
        # Step 3: Register new model
        model_id = self.registry.register_model(
            model=training_results['model'],
            name=model_name,
            version=new_version,
            model_type=ModelType.CLASSIFIER,
            description=f"Auto-retrained model. Previous version: {current_version}",
            author="Automated Pipeline",
            performance_metrics=training_results['metrics']['test'],
            hyperparameters=hyperparameters,
            stage=ModelStage.DEVELOPMENT
        )
        
        # Step 4: Compare and promote
        promotion_result = self.compare_and_promote(
            model_name, new_version, current_version
        )
        
        return {
            'retrained': True,
            'new_version': new_version,
            'model_id': model_id,
            'training_results': training_results,
            'promotion_result': promotion_result,
            'retrain_info': retrain_info
        }

