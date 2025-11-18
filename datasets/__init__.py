"""Dataset loaders and utilities for ML showcase"""

from .loaders import (
    load_wine_quality,
    load_breast_cancer,
    load_credit_card_fraud,
    load_housing_prices,
    load_contract_classification,
    list_available_datasets
)

__all__ = [
    'load_wine_quality',
    'load_breast_cancer',
    'load_credit_card_fraud',
    'load_housing_prices',
    'load_contract_classification',
    'list_available_datasets'
]

