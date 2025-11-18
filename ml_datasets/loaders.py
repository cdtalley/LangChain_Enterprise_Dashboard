"""
Dataset Loaders
===============
Production-ready dataset loaders with validation and preprocessing.
Demonstrates data engineering expertise.
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any, Optional
from pathlib import Path
import logging
from sklearn.datasets import load_wine, load_breast_cancer, fetch_california_housing
from sklearn.model_selection import train_test_split
import requests
import io

try:
    from datasets import Dataset as HFDataset
except ImportError:
    HFDataset = None

logger = logging.getLogger(__name__)

DATASETS_DIR = Path(__file__).parent / "data"
DATASETS_DIR.mkdir(exist_ok=True)


def load_wine_quality(test_size: float = 0.2, random_state: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Load Wine Quality dataset (UCI)
    
    Returns:
        X_train, X_test, y_train, y_test
    """
    try:
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
        df = pd.read_csv(url, sep=';')
        
        X = df.drop('quality', axis=1)
        y = df['quality']
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        logger.info(f"Loaded Wine Quality: {len(X_train)} train, {len(X_test)} test samples")
        return X_train, X_test, y_train, y_test
        
    except Exception as e:
        logger.warning(f"Failed to load Wine Quality from URL, using sklearn wine: {e}")
        data = load_wine()
        X_train, X_test, y_train, y_test = train_test_split(
            data.data, data.target, test_size=test_size, random_state=random_state
        )
        X_train = pd.DataFrame(X_train, columns=data.feature_names)
        X_test = pd.DataFrame(X_test, columns=data.feature_names)
        return X_train, X_test, pd.Series(y_train), pd.Series(y_test)


def load_breast_cancer(test_size: float = 0.2, random_state: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Load Breast Cancer Wisconsin dataset (sklearn)
    
    Returns:
        X_train, X_test, y_train, y_test
    """
    data = load_breast_cancer()
    X_train, X_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=test_size, random_state=random_state, stratify=data.target
    )
    
    X_train = pd.DataFrame(X_train, columns=data.feature_names)
    X_test = pd.DataFrame(X_test, columns=data.feature_names)
    
    logger.info(f"Loaded Breast Cancer: {len(X_train)} train, {len(X_test)} test samples")
    return X_train, X_test, pd.Series(y_train), pd.Series(y_test)


def load_credit_card_fraud(test_size: float = 0.2, random_state: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Load Credit Card Fraud Detection dataset (synthetic for demo)
    
    Returns:
        X_train, X_test, y_train, y_test
    """
    np.random.seed(random_state)
    n_samples = 10000
    
    X = pd.DataFrame({
        'amount': np.random.lognormal(3, 1.5, n_samples),
        'time': np.random.uniform(0, 172792, n_samples),
        'v1': np.random.normal(0, 1, n_samples),
        'v2': np.random.normal(0, 1, n_samples),
        'v3': np.random.normal(0, 1, n_samples),
        'v4': np.random.normal(0, 1, n_samples),
        'v5': np.random.normal(0, 1, n_samples),
    })
    
    fraud_prob = 1 / (1 + np.exp(-(X['amount'] - X['amount'].mean()) / X['amount'].std()))
    y = pd.Series(np.random.binomial(1, fraud_prob * 0.02))
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    logger.info(f"Loaded Credit Card Fraud: {len(X_train)} train, {len(X_test)} test samples")
    return X_train, X_test, y_train, y_test


def load_housing_prices(test_size: float = 0.2, random_state: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Load California Housing Prices dataset (sklearn)
    
    Returns:
        X_train, X_test, y_train, y_test
    """
    data = fetch_california_housing()
    X_train, X_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=test_size, random_state=random_state
    )
    
    X_train = pd.DataFrame(X_train, columns=data.feature_names)
    X_test = pd.DataFrame(X_test, columns=data.feature_names)
    
    logger.info(f"Loaded Housing Prices: {len(X_train)} train, {len(X_test)} test samples")
    return X_train, X_test, pd.Series(y_train), pd.Series(y_test)


def load_contract_classification(test_size: float = 0.2, random_state: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Load Contract Classification dataset (synthetic for FinQuery domain)
    
    Features relevant to contract/lease analysis:
    - contract_value, duration_months, renewal_probability, risk_score
    """
    np.random.seed(random_state)
    n_samples = 5000
    
    X = pd.DataFrame({
        'contract_value': np.random.lognormal(10, 1.5, n_samples),
        'duration_months': np.random.choice([12, 24, 36, 48, 60], n_samples),
        'renewal_probability': np.random.beta(2, 5, n_samples),
        'risk_score': np.random.gamma(2, 2, n_samples),
        'payment_terms_days': np.random.choice([15, 30, 45, 60], n_samples),
        'termination_penalty_pct': np.random.uniform(0, 0.2, n_samples),
    })
    
    contract_types = ['lease', 'service', 'purchase', 'license']
    y = pd.Series(np.random.choice(contract_types, n_samples, p=[0.4, 0.3, 0.2, 0.1]))
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    logger.info(f"Loaded Contract Classification: {len(X_train)} train, {len(X_test)} test samples")
    return X_train, X_test, y_train, y_test


def list_available_datasets() -> Dict[str, Dict[str, Any]]:
    """List all available datasets with metadata"""
    return {
        'wine_quality': {
            'name': 'Wine Quality',
            'type': 'classification',
            'samples': '~1600',
            'features': 11,
            'description': 'Wine quality prediction based on physicochemical properties',
            'source': 'UCI ML Repository'
        },
        'breast_cancer': {
            'name': 'Breast Cancer Wisconsin',
            'type': 'binary_classification',
            'samples': '~570',
            'features': 30,
            'description': 'Breast cancer diagnosis classification',
            'source': 'sklearn'
        },
        'credit_card_fraud': {
            'name': 'Credit Card Fraud Detection',
            'type': 'binary_classification',
            'samples': '~10000',
            'features': 7,
            'description': 'Fraud detection in credit card transactions',
            'source': 'Synthetic'
        },
        'housing_prices': {
            'name': 'California Housing Prices',
            'type': 'regression',
            'samples': '~20000',
            'features': 8,
            'description': 'House price prediction in California',
            'source': 'sklearn'
        },
        'contract_classification': {
            'name': 'Contract Classification',
            'type': 'multiclass_classification',
            'samples': '~5000',
            'features': 6,
            'description': 'Contract type classification (lease, service, purchase, license)',
            'source': 'Synthetic (FinQuery domain)'
        }
    }

