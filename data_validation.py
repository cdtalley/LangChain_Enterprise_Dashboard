"""
Data Validation Pipeline
========================
Production-ready data validation for MLOps.
Demonstrates MLOps skills in:
- Schema validation
- Data quality checks
- Drift detection
- Anomaly detection
- Data profiling
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
import logging
from pydantic import BaseModel, Field, validator
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Validation result"""
    passed: bool
    errors: List[str]
    warnings: List[str]
    statistics: Dict[str, Any]


class DataSchema(BaseModel):
    """Data schema definition"""
    columns: Dict[str, str] = Field(..., description="Column name to type mapping")
    required_columns: List[str] = Field(default_factory=list)
    nullable_columns: List[str] = Field(default_factory=list)
    value_constraints: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    
    @validator('columns')
    def validate_column_types(cls, v):
        valid_types = ['int', 'float', 'str', 'bool', 'datetime', 'category']
        for col, col_type in v.items():
            if col_type not in valid_types:
                raise ValueError(f"Invalid type {col_type} for column {col}")
        return v


class DataValidator:
    """
    Production Data Validator
    
    Features:
    - Schema validation
    - Data quality checks
    - Missing value detection
    - Outlier detection
    - Distribution checks
    """
    
    def __init__(self, schema: Optional[DataSchema] = None):
        self.schema = schema
        logger.info("Data Validator initialized")
    
    def validate_schema(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """Validate DataFrame against schema"""
        if not self.schema:
            return True, []
        
        errors = []
        
        # Check required columns
        missing_cols = set(self.schema.required_columns) - set(df.columns)
        if missing_cols:
            errors.append(f"Missing required columns: {missing_cols}")
        
        # Check column types
        for col, expected_type in self.schema.columns.items():
            if col not in df.columns:
                continue
            
            actual_type = str(df[col].dtype)
            type_mapping = {
                'int': 'int64',
                'float': 'float64',
                'str': 'object',
                'bool': 'bool',
                'datetime': 'datetime64[ns]',
                'category': 'category'
            }
            
            expected_dtype = type_mapping.get(expected_type)
            if expected_dtype and expected_dtype not in actual_type:
                errors.append(f"Column {col} has type {actual_type}, expected {expected_type}")
        
        return len(errors) == 0, errors
    
    def validate_data_quality(self, df: pd.DataFrame) -> ValidationResult:
        """Comprehensive data quality validation"""
        errors = []
        warnings = []
        statistics = {}
        
        # Missing values check
        missing_counts = df.isnull().sum()
        missing_pct = (missing_counts / len(df)) * 100
        
        for col, pct in missing_pct.items():
            if pct > 50:
                errors.append(f"Column {col} has {pct:.1f}% missing values")
            elif pct > 10:
                warnings.append(f"Column {col} has {pct:.1f}% missing values")
        
        statistics['missing_values'] = missing_counts.to_dict()
        statistics['missing_percentages'] = missing_pct.to_dict()
        
        # Duplicate rows check
        duplicate_count = df.duplicated().sum()
        if duplicate_count > 0:
            duplicate_pct = (duplicate_count / len(df)) * 100
            if duplicate_pct > 10:
                warnings.append(f"{duplicate_pct:.1f}% duplicate rows detected")
            statistics['duplicate_rows'] = int(duplicate_count)
        
        # Outlier detection (for numerical columns)
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        outlier_stats = {}
        
        for col in numerical_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            outlier_count = len(outliers)
            outlier_pct = (outlier_count / len(df)) * 100
            
            if outlier_pct > 5:
                warnings.append(f"Column {col} has {outlier_pct:.1f}% outliers")
            
            outlier_stats[col] = {
                'count': int(outlier_count),
                'percentage': float(outlier_pct),
                'lower_bound': float(lower_bound),
                'upper_bound': float(upper_bound)
            }
        
        statistics['outliers'] = outlier_stats
        
        # Value constraints check
        if self.schema and self.schema.value_constraints:
            for col, constraints in self.schema.value_constraints.items():
                if col not in df.columns:
                    continue
                
                if 'min' in constraints:
                    below_min = (df[col] < constraints['min']).sum()
                    if below_min > 0:
                        errors.append(f"Column {col} has {below_min} values below minimum {constraints['min']}")
                
                if 'max' in constraints:
                    above_max = (df[col] > constraints['max']).sum()
                    if above_max > 0:
                        errors.append(f"Minimum sample size: {min_sample_size}")
                
                if 'allowed_values' in constraints:
                    invalid = ~df[col].isin(constraints['allowed_values'])
                    invalid_count = invalid.sum()
                    if invalid_count > 0:
                        errors.append(f"Column {col} has {invalid_count} invalid values")
        
        # Data distribution statistics
        statistics['shape'] = {'rows': len(df), 'columns': len(df.columns)}
        statistics['dtypes'] = df.dtypes.astype(str).to_dict()
        
        for col in numerical_cols:
            statistics[f'{col}_stats'] = {
                'mean': float(df[col].mean()),
                'std': float(df[col].std()),
                'min': float(df[col].min()),
                'max': float(df[col].max()),
                'median': float(df[col].median())
            }
        
        passed = len(errors) == 0
        
        return ValidationResult(
            passed=passed,
            errors=errors,
            warnings=warnings,
            statistics=statistics
        )
    
    def detect_drift(
        self,
        reference_df: pd.DataFrame,
        current_df: pd.DataFrame,
        threshold: float = 0.1
    ) -> Dict[str, Any]:
        """Detect data drift between reference and current data"""
        drift_results = {}
        
        # Compare distributions for numerical columns
        numerical_cols = reference_df.select_dtypes(include=[np.number]).columns
        
        for col in numerical_cols:
            if col not in current_df.columns:
                continue
            
            ref_mean = reference_df[col].mean()
            ref_std = reference_df[col].std()
            curr_mean = current_df[col].mean()
            curr_std = current_df[col].std()
            
            # Calculate drift score (normalized difference)
            mean_drift = abs(curr_mean - ref_mean) / (ref_std + 1e-10)
            std_drift = abs(curr_std - ref_std) / (ref_std + 1e-10)
            
            drift_score = max(mean_drift, std_drift)
            
            drift_results[col] = {
                'drift_score': float(drift_score),
                'drift_detected': drift_score > threshold,
                'reference_mean': float(ref_mean),
                'current_mean': float(curr_mean),
                'reference_std': float(ref_std),
                'current_std': float(curr_std)
            }
        
        # Compare distributions for categorical columns
        categorical_cols = reference_df.select_dtypes(include=['object', 'category']).columns
        
        for col in categorical_cols:
            if col not in current_df.columns:
                continue
            
            ref_dist = reference_df[col].value_counts(normalize=True)
            curr_dist = current_df[col].value_counts(normalize=True)
            
            # Calculate PSI (Population Stability Index)
            all_categories = set(ref_dist.index) | set(curr_dist.index)
            psi = 0.0
            
            for cat in all_categories:
                ref_pct = ref_dist.get(cat, 0.0001)
                curr_pct = curr_dist.get(cat, 0.0001)
                psi += (curr_pct - ref_pct) * np.log(curr_pct / ref_pct)
            
            drift_results[col] = {
                'drift_score': float(psi),
                'drift_detected': psi > threshold,
                'psi': float(psi)
            }
        
        return drift_results
    
    def generate_profile(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate comprehensive data profile"""
        profile = {
            'overview': {
                'num_rows': len(df),
                'num_columns': len(df.columns),
                'memory_usage_mb': float(df.memory_usage(deep=True).sum() / 1024**2)
            },
            'columns': {}
        }
        
        for col in df.columns:
            col_profile = {
                'dtype': str(df[col].dtype),
                'null_count': int(df[col].isnull().sum()),
                'null_percentage': float(df[col].isnull().sum() / len(df) * 100),
                'unique_count': int(df[col].nunique())
            }
            
            if df[col].dtype in ['int64', 'float64']:
                col_profile['statistics'] = {
                    'mean': float(df[col].mean()),
                    'std': float(df[col].std()),
                    'min': float(df[col].min()),
                    'max': float(df[col].max()),
                    'median': float(df[col].median()),
                    'q25': float(df[col].quantile(0.25)),
                    'q75': float(df[col].quantile(0.75))
                }
            elif df[col].dtype == 'object':
                col_profile['top_values'] = df[col].value_counts().head(10).to_dict()
            
            profile['columns'][col] = col_profile
        
        return profile

