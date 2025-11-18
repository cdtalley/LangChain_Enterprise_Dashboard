"""
Model Training Scripts
======================
Train models on datasets and register them in the model registry.
Demonstrates end-to-end ML workflow.
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from ml_datasets.loaders import (
    load_wine_quality, load_breast_cancer, load_credit_card_fraud,
    load_housing_prices, load_contract_classification
)
from model_registry import ModelRegistryManager, ModelType, ModelStage
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, mean_squared_error, r2_score
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def train_wine_quality_model():
    """Train wine quality classifier"""
    logger.info("Training Wine Quality model...")
    X_train, X_test, y_train, y_test = load_wine_quality()
    
    model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    registry = ModelRegistryManager()
    model_id = registry.register_model(
        name="wine-quality-classifier",
        version="1.0.0",
        model=model,
        model_type=ModelType.CLASSIFIER,
        stage=ModelStage.DEVELOPMENT,
        performance_metrics={
            'accuracy': float(accuracy),
            'f1_score': float(f1),
            'test_samples': len(X_test)
        },
        hyperparameters={
            'n_estimators': 100,
            'max_depth': 10,
            'random_state': 42
        },
        feature_order=list(X_train.columns)
    )
    
    logger.info(f"✅ Wine Quality model registered: {model_id}")
    return model_id


def train_breast_cancer_model():
    """Train breast cancer classifier"""
    logger.info("Training Breast Cancer model...")
    X_train, X_test, y_train, y_test = load_breast_cancer()
    
    model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=15)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    registry = ModelRegistryManager()
    model_id = registry.register_model(
        name="breast-cancer-classifier",
        version="1.0.0",
        model=model,
        model_type=ModelType.CLASSIFIER,
        stage=ModelStage.DEVELOPMENT,
        performance_metrics={
            'accuracy': float(accuracy),
            'precision': float(precision),
            'recall': float(recall),
            'f1_score': float(f1),
            'test_samples': len(X_test)
        },
        hyperparameters={
            'n_estimators': 100,
            'max_depth': 15,
            'random_state': 42
        },
        feature_order=list(X_train.columns)
    )
    
    logger.info(f"✅ Breast Cancer model registered: {model_id}")
    return model_id


def train_credit_card_fraud_model():
    """Train credit card fraud detector"""
    logger.info("Training Credit Card Fraud model...")
    X_train, X_test, y_train, y_test = load_credit_card_fraud()
    
    model = RandomForestClassifier(n_estimators=200, random_state=42, class_weight='balanced')
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    
    registry = ModelRegistryManager()
    model_id = registry.register_model(
        name="credit-card-fraud-detector",
        version="1.0.0",
        model=model,
        model_type=ModelType.CLASSIFIER,
        stage=ModelStage.DEVELOPMENT,
        performance_metrics={
            'accuracy': float(accuracy),
            'precision': float(precision),
            'recall': float(recall),
            'f1_score': float(f1),
            'test_samples': len(X_test)
        },
        hyperparameters={
            'n_estimators': 200,
            'class_weight': 'balanced',
            'random_state': 42
        },
        feature_order=list(X_train.columns)
    )
    
    logger.info(f"✅ Credit Card Fraud model registered: {model_id}")
    return model_id


def train_housing_prices_model():
    """Train housing prices regressor"""
    logger.info("Training Housing Prices model...")
    X_train, X_test, y_train, y_test = load_housing_prices()
    
    model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=20)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    registry = ModelRegistryManager()
    model_id = registry.register_model(
        name="housing-prices-regressor",
        version="1.0.0",
        model=model,
        model_type=ModelType.REGRESSOR,
        stage=ModelStage.DEVELOPMENT,
        performance_metrics={
            'mse': float(mse),
            'rmse': float(rmse),
            'r2_score': float(r2),
            'test_samples': len(X_test)
        },
        hyperparameters={
            'n_estimators': 100,
            'max_depth': 20,
            'random_state': 42
        },
        feature_order=list(X_train.columns)
    )
    
    logger.info(f"✅ Housing Prices model registered: {model_id}")
    return model_id


def train_contract_classification_model():
    """Train contract classification model (FinQuery domain)"""
    logger.info("Training Contract Classification model...")
    X_train, X_test, y_train, y_test = load_contract_classification()
    
    model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=15)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    registry = ModelRegistryManager()
    model_id = registry.register_model(
        name="contract-classifier",
        version="1.0.0",
        model=model,
        model_type=ModelType.CLASSIFIER,
        stage=ModelStage.DEVELOPMENT,
        performance_metrics={
            'accuracy': float(accuracy),
            'f1_score': float(f1),
            'test_samples': len(X_test)
        },
        hyperparameters={
            'n_estimators': 100,
            'max_depth': 15,
            'random_state': 42
        },
        feature_order=list(X_train.columns),
        tags=['finquery', 'contracts', 'leases']
    )
    
    logger.info(f"✅ Contract Classification model registered: {model_id}")
    return model_id


def train_all_models():
    """Train all available models"""
    logger.info("🚀 Training all models...")
    results = {}
    
    try:
        results['wine_quality'] = train_wine_quality_model()
    except Exception as e:
        logger.error(f"Failed to train wine quality model: {e}")
    
    try:
        results['breast_cancer'] = train_breast_cancer_model()
    except Exception as e:
        logger.error(f"Failed to train breast cancer model: {e}")
    
    try:
        results['credit_card_fraud'] = train_credit_card_fraud_model()
    except Exception as e:
        logger.error(f"Failed to train credit card fraud model: {e}")
    
    try:
        results['housing_prices'] = train_housing_prices_model()
    except Exception as e:
        logger.error(f"Failed to train housing prices model: {e}")
    
    try:
        results['contract_classification'] = train_contract_classification_model()
    except Exception as e:
        logger.error(f"Failed to train contract classification model: {e}")
    
    logger.info(f"✅ Training complete. Registered {len(results)} models.")
    return results


if __name__ == "__main__":
    train_all_models()

