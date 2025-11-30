"""Generate realistic demo data for various industries."""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import random


class DemoDataGenerator:
    """Generate realistic demo datasets for different industries."""
    
    def __init__(self, seed: int = 42):
        np.random.seed(seed)
        random.seed(seed)
    
    def generate_healthcare_data(self, n_records: int = 1000) -> pd.DataFrame:
        """Generate healthcare patient data."""
        conditions = ['Hypertension', 'Diabetes', 'Asthma', 'Arthritis', 'Heart Disease', 'Obesity']
        medications = ['Metformin', 'Lisinopril', 'Albuterol', 'Ibuprofen', 'Aspirin', 'Atorvastatin']
        
        data = {
            'patient_id': [f'PAT-{i:04d}' for i in range(1, n_records + 1)],
            'age': np.random.normal(45, 15, n_records).astype(int).clip(18, 90),
            'gender': np.random.choice(['M', 'F'], n_records),
            'bmi': np.random.normal(26, 5, n_records).round(1).clip(18, 40),
            'blood_pressure_systolic': np.random.normal(120, 15, n_records).astype(int).clip(90, 180),
            'blood_pressure_diastolic': np.random.normal(80, 10, n_records).astype(int).clip(60, 120),
            'cholesterol': np.random.normal(200, 40, n_records).astype(int).clip(100, 300),
            'glucose': np.random.normal(100, 20, n_records).astype(int).clip(70, 200),
            'condition': np.random.choice(conditions, n_records, p=[0.25, 0.20, 0.15, 0.15, 0.15, 0.10]),
            'medication': np.random.choice(medications, n_records),
            'visit_date': pd.date_range(start='2023-01-01', periods=n_records, freq='D'),
            'cost': np.random.lognormal(5, 1, n_records).round(2),
            'readmission_risk': np.random.choice([0, 1], n_records, p=[0.85, 0.15])
        }
        
        return pd.DataFrame(data)
    
    def generate_finance_data(self, n_records: int = 1000) -> pd.DataFrame:
        """Generate financial transaction data."""
        transaction_types = ['Purchase', 'Transfer', 'Deposit', 'Withdrawal', 'Payment', 'Refund']
        categories = ['Groceries', 'Restaurants', 'Shopping', 'Transport', 'Bills', 'Entertainment', 'Healthcare']
        merchants = ['Amazon', 'Walmart', 'Target', 'Starbucks', 'Shell', 'AT&T', 'Netflix', 'CVS']
        
        data = {
            'transaction_id': [f'TXN-{i:06d}' for i in range(1, n_records + 1)],
            'customer_id': [f'CUST-{np.random.randint(1000, 9999)}' for _ in range(n_records)],
            'date': pd.date_range(start='2024-01-01', periods=n_records, freq='H'),
            'transaction_type': np.random.choice(transaction_types, n_records, p=[0.40, 0.15, 0.15, 0.10, 0.15, 0.05]),
            'category': np.random.choice(categories, n_records),
            'merchant': np.random.choice(merchants, n_records),
            'amount': np.random.lognormal(3.5, 1.2, n_records).round(2),
            'currency': 'USD',
            'is_fraud': np.random.choice([0, 1], n_records, p=[0.97, 0.03]),
            'account_balance': np.random.normal(5000, 2000, n_records).round(2),
            'credit_score': np.random.normal(720, 50, n_records).astype(int).clip(300, 850)
        }
        
        return pd.DataFrame(data)
    
    def generate_ecommerce_data(self, n_records: int = 1000) -> pd.DataFrame:
        """Generate e-commerce sales data."""
        products = ['Laptop', 'Smartphone', 'Headphones', 'Tablet', 'Smartwatch', 'Camera', 'Speaker', 'Monitor']
        categories = ['Electronics', 'Computers', 'Audio', 'Mobile', 'Wearables', 'Photography', 'Accessories']
        regions = ['North', 'South', 'East', 'West', 'Central']
        
        data = {
            'order_id': [f'ORD-{i:06d}' for i in range(1, n_records + 1)],
            'customer_id': [f'CUST-{np.random.randint(1000, 9999)}' for _ in range(n_records)],
            'product': np.random.choice(products, n_records),
            'category': np.random.choice(categories, n_records),
            'order_date': pd.date_range(start='2024-01-01', periods=n_records, freq='H'),
            'quantity': np.random.poisson(2, n_records).clip(1, 10),
            'unit_price': np.random.lognormal(4, 1, n_records).round(2),
            'total_amount': None,
            'region': np.random.choice(regions, n_records),
            'payment_method': np.random.choice(['Credit Card', 'Debit Card', 'PayPal', 'Apple Pay'], n_records),
            'shipping_cost': np.random.choice([0, 5.99, 9.99, 14.99], n_records, p=[0.3, 0.4, 0.2, 0.1]),
            'discount': np.random.choice([0, 0.05, 0.10, 0.15, 0.20], n_records, p=[0.5, 0.2, 0.15, 0.10, 0.05]),
            'returned': np.random.choice([0, 1], n_records, p=[0.92, 0.08])
        }
        
        df = pd.DataFrame(data)
        df['total_amount'] = (df['quantity'] * df['unit_price'] * (1 - df['discount']) + df['shipping_cost']).round(2)
        return df
    
    def generate_manufacturing_data(self, n_records: int = 1000) -> pd.DataFrame:
        """Generate manufacturing production data."""
        products = ['Widget A', 'Widget B', 'Widget C', 'Component X', 'Component Y', 'Assembly Z']
        machines = ['Machine-01', 'Machine-02', 'Machine-03', 'Machine-04', 'Machine-05']
        operators = [f'OP-{i:02d}' for i in range(1, 21)]
        
        data = {
            'batch_id': [f'BATCH-{i:05d}' for i in range(1, n_records + 1)],
            'product': np.random.choice(products, n_records),
            'machine_id': np.random.choice(machines, n_records),
            'operator_id': np.random.choice(operators, n_records),
            'production_date': pd.date_range(start='2024-01-01', periods=n_records, freq='H'),
            'quantity_produced': np.random.poisson(100, n_records).clip(50, 200),
            'target_quantity': 100,
            'production_time_minutes': np.random.normal(120, 20, n_records).round(1).clip(60, 180),
            'temperature': np.random.normal(75, 5, n_records).round(1).clip(65, 85),
            'pressure': np.random.normal(15, 2, n_records).round(1).clip(10, 20),
            'quality_score': np.random.normal(95, 5, n_records).round(1).clip(80, 100),
            'defect_count': np.random.poisson(2, n_records).clip(0, 10),
            'defect_rate': None,
            'material_cost': np.random.normal(500, 100, n_records).round(2),
            'labor_cost': np.random.normal(200, 50, n_records).round(2)
        }
        
        df = pd.DataFrame(data)
        df['defect_rate'] = (df['defect_count'] / df['quantity_produced'] * 100).round(2)
        df['total_cost'] = (df['material_cost'] + df['labor_cost']).round(2)
        return df
    
    def generate_marketing_data(self, n_records: int = 1000) -> pd.DataFrame:
        """Generate marketing campaign data."""
        channels = ['Email', 'Social Media', 'Search Ads', 'Display Ads', 'TV', 'Radio', 'Print']
        campaigns = ['Summer Sale', 'Black Friday', 'Holiday Special', 'New Product Launch', 'Brand Awareness']
        regions = ['North America', 'Europe', 'Asia', 'South America', 'Oceania']
        
        data = {
            'campaign_id': [f'CAMP-{i:04d}' for i in range(1, n_records + 1)],
            'campaign_name': np.random.choice(campaigns, n_records),
            'channel': np.random.choice(channels, n_records),
            'region': np.random.choice(regions, n_records),
            'date': pd.date_range(start='2024-01-01', periods=n_records, freq='D'),
            'impressions': np.random.poisson(10000, n_records).clip(1000, 50000),
            'clicks': None,
            'conversions': None,
            'spend': np.random.lognormal(6, 1, n_records).round(2),
            'revenue': None,
            'ctr': None,
            'conversion_rate': None,
            'roas': None
        }
        
        df = pd.DataFrame(data)
        df['clicks'] = (df['impressions'] * np.random.uniform(0.01, 0.05, n_records)).astype(int)
        df['conversions'] = (df['clicks'] * np.random.uniform(0.02, 0.10, n_records)).astype(int)
        df['revenue'] = (df['conversions'] * np.random.uniform(50, 200, n_records)).round(2)
        df['ctr'] = (df['clicks'] / df['impressions'] * 100).round(2)
        df['conversion_rate'] = (df['conversions'] / df['clicks'] * 100).round(2)
        df['roas'] = (df['revenue'] / df['spend']).round(2)
        return df
    
    def generate_real_estate_data(self, n_records: int = 1000) -> pd.DataFrame:
        """Generate real estate listing data."""
        property_types = ['House', 'Apartment', 'Condo', 'Townhouse', 'Villa']
        neighborhoods = ['Downtown', 'Suburbs', 'Waterfront', 'Hills', 'Historic District', 'Business District']
        cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio']
        
        data = {
            'listing_id': [f'LIST-{i:05d}' for i in range(1, n_records + 1)],
            'property_type': np.random.choice(property_types, n_records),
            'city': np.random.choice(cities, n_records),
            'neighborhood': np.random.choice(neighborhoods, n_records),
            'bedrooms': np.random.choice([1, 2, 3, 4, 5], n_records, p=[0.1, 0.2, 0.3, 0.3, 0.1]),
            'bathrooms': np.random.choice([1, 1.5, 2, 2.5, 3, 4], n_records, p=[0.15, 0.15, 0.25, 0.20, 0.15, 0.10]),
            'sqft': np.random.normal(2000, 800, n_records).astype(int).clip(500, 5000),
            'lot_size': np.random.normal(0.25, 0.15, n_records).round(2).clip(0.05, 1.0),
            'year_built': np.random.randint(1950, 2024, n_records),
            'price': None,
            'price_per_sqft': None,
            'days_on_market': np.random.poisson(30, n_records).clip(1, 180),
            'sold': np.random.choice([0, 1], n_records, p=[0.3, 0.7]),
            'sale_date': None
        }
        
        df = pd.DataFrame(data)
        base_price = df['sqft'] * np.random.uniform(150, 400, n_records)
        df['price'] = (base_price + df['bedrooms'] * 20000 + df['bathrooms'] * 15000).round(0)
        df['price_per_sqft'] = (df['price'] / df['sqft']).round(2)
        
        sold_mask = df['sold'] == 1
        if sold_mask.any():
            df.loc[sold_mask, 'sale_date'] = pd.date_range(
                start='2024-01-01', 
                periods=sold_mask.sum(), 
                freq='D'
            )
        
        return df
    
    def generate_hr_data(self, n_records: int = 1000) -> pd.DataFrame:
        """Generate HR/employee data."""
        departments = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations', 'Product']
        job_titles = ['Junior', 'Mid-Level', 'Senior', 'Lead', 'Manager', 'Director', 'VP']
        locations = ['New York', 'San Francisco', 'Austin', 'Seattle', 'Boston', 'Remote']
        
        data = {
            'employee_id': [f'EMP-{i:05d}' for i in range(1, n_records + 1)],
            'name': [f'Employee {i}' for i in range(1, n_records + 1)],
            'department': np.random.choice(departments, n_records),
            'job_title': np.random.choice(job_titles, n_records),
            'location': np.random.choice(locations, n_records),
            'hire_date': pd.date_range(start='2015-01-01', periods=n_records, freq='D'),
            'age': np.random.normal(35, 10, n_records).astype(int).clip(22, 65),
            'years_experience': np.random.normal(8, 5, n_records).round(1).clip(0, 30),
            'salary': None,
            'performance_score': np.random.normal(85, 10, n_records).round(1).clip(60, 100),
            'satisfaction_score': np.random.normal(7.5, 1.5, n_records).round(1).clip(1, 10),
            'projects_completed': np.random.poisson(5, n_records).clip(0, 20),
            'training_hours': np.random.poisson(20, n_records).clip(0, 100),
            'promoted': np.random.choice([0, 1], n_records, p=[0.7, 0.3]),
            'left_company': np.random.choice([0, 1], n_records, p=[0.85, 0.15])
        }
        
        df = pd.DataFrame(data)
        base_salary = 50000 + df['years_experience'] * 5000
        title_multiplier = {'Junior': 1.0, 'Mid-Level': 1.3, 'Senior': 1.6, 'Lead': 2.0, 
                           'Manager': 2.5, 'Director': 3.5, 'VP': 5.0}
        df['salary'] = (base_salary * df['job_title'].map(title_multiplier)).round(0)
        return df
    
    def generate_supply_chain_data(self, n_records: int = 1000) -> pd.DataFrame:
        """Generate supply chain logistics data."""
        suppliers = [f'Supplier-{i:02d}' for i in range(1, 21)]
        products = ['Raw Material A', 'Raw Material B', 'Component C', 'Component D', 'Packaging']
        destinations = ['Warehouse-1', 'Warehouse-2', 'Warehouse-3', 'Distribution Center', 'Retail Store']
        
        data = {
            'shipment_id': [f'SHIP-{i:06d}' for i in range(1, n_records + 1)],
            'supplier': np.random.choice(suppliers, n_records),
            'product': np.random.choice(products, n_records),
            'destination': np.random.choice(destinations, n_records),
            'ship_date': pd.date_range(start='2024-01-01', periods=n_records, freq='H'),
            'quantity': np.random.poisson(100, n_records).clip(10, 500),
            'unit_cost': np.random.lognormal(3, 1, n_records).round(2),
            'total_cost': None,
            'transit_days': np.random.poisson(5, n_records).clip(1, 14),
            'delivery_date': None,
            'on_time': None,
            'damage_rate': np.random.uniform(0, 0.05, n_records).round(3),
            'temperature': np.random.normal(20, 5, n_records).round(1).clip(-10, 30),
            'quality_score': np.random.normal(95, 5, n_records).round(1).clip(80, 100)
        }
        
        df = pd.DataFrame(data)
        df['total_cost'] = (df['quantity'] * df['unit_cost']).round(2)
        df['delivery_date'] = df['ship_date'] + pd.to_timedelta(df['transit_days'], unit='D')
        df['on_time'] = (df['transit_days'] <= 7).astype(int)
        return df
    
    def get_available_datasets(self) -> Dict[str, Dict]:
        """Get list of available demo datasets."""
        return {
            'Healthcare': {
                'function': self.generate_healthcare_data,
                'description': 'Patient records, vitals, conditions, medications',
                'icon': '🏥',
                'size': '1000 records'
            },
            'Finance': {
                'function': self.generate_finance_data,
                'description': 'Transactions, fraud detection, customer data',
                'icon': '💳',
                'size': '1000 records'
            },
            'E-commerce': {
                'function': self.generate_ecommerce_data,
                'description': 'Sales, products, orders, customer behavior',
                'icon': '🛒',
                'size': '1000 records'
            },
            'Manufacturing': {
                'function': self.generate_manufacturing_data,
                'description': 'Production batches, quality metrics, defects',
                'icon': '🏭',
                'size': '1000 records'
            },
            'Marketing': {
                'function': self.generate_marketing_data,
                'description': 'Campaigns, conversions, ROI, channel performance',
                'icon': '📢',
                'size': '1000 records'
            },
            'Real Estate': {
                'function': self.generate_real_estate_data,
                'description': 'Property listings, sales, market data',
                'icon': '🏠',
                'size': '1000 records'
            },
            'HR': {
                'function': self.generate_hr_data,
                'description': 'Employee data, performance, retention',
                'icon': '👥',
                'size': '1000 records'
            },
            'Supply Chain': {
                'function': self.generate_supply_chain_data,
                'description': 'Shipments, logistics, supplier data',
                'icon': '🚚',
                'size': '1000 records'
            }
        }
    
    def generate_dataset(self, industry: str, n_records: int = 1000) -> pd.DataFrame:
        """Generate dataset for specified industry."""
        datasets = self.get_available_datasets()
        if industry not in datasets:
            raise ValueError(f"Unknown industry: {industry}")
        
        return datasets[industry]['function'](n_records)

