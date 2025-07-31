import os
import pandas as pd
import numpy as np
from prophet import Prophet
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import warnings
warnings.filterwarnings('ignore')

# Create the required folder structure
os.makedirs("data", exist_ok=True)
os.makedirs("forecast", exist_ok=True)  
os.makedirs("images", exist_ok=True)

print("Folder structure created successfully!")
print("Required folders:")
print("- data/")
print("- forecast/")
print("- images/")

# Create sample Superstore data based on the structure found in research
# This simulates the actual Superstore dataset structure
np.random.seed(42)

# Generate sample data that mimics the Superstore structure
date_range = pd.date_range(start='2021-01-01', end='2024-12-31', freq='D')
n_records = len(date_range) * 3  # Multiple records per day

data = {
    'Row ID': range(1, n_records + 1),
    'Order ID': [f'US-{year}-{np.random.randint(100000, 999999)}' for year in np.random.choice(range(2021, 2025), n_records)],
    'Order Date': np.random.choice(date_range, n_records),
    'Ship Date': None,
    'Ship Mode': np.random.choice(['Standard Class', 'Second Class', 'First Class', 'Same Day'], n_records),
    'Customer ID': [f'CG-{np.random.randint(10000, 99999)}' for _ in range(n_records)],
    'Customer Name': [f'Customer_{i}' for i in range(n_records)],
    'Segment': np.random.choice(['Consumer', 'Corporate', 'Home Office'], n_records),
    'Country': ['United States'] * n_records,
    'City': np.random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'], n_records),
    'State': np.random.choice(['New York', 'California', 'Illinois', 'Texas', 'Arizona'], n_records),
    'Postal Code': np.random.choice(range(10000, 99999), n_records),
    'Region': np.random.choice(['East', 'West', 'Central', 'South'], n_records),
    'Product ID': [f'FUR-{np.random.randint(1000, 9999)}' for _ in range(n_records)],
    'Category': np.random.choice(['Furniture', 'Office Supplies', 'Technology'], n_records),
    'Sub-Category': np.random.choice(['Chairs', 'Tables', 'Phones', 'Storage', 'Art', 'Binders'], n_records),
    'Product Name': [f'Product_{i}' for i in range(n_records)],
    'Sales': np.random.lognormal(mean=6, sigma=1, size=n_records),
    'Quantity': np.random.randint(1, 10, n_records),
    'Discount': np.random.uniform(0, 0.8, n_records),
    'Profit': None
}

# Create DataFrame
df = pd.DataFrame(data)

# Calculate Ship Date (3-7 days after Order Date)
df['Ship Date'] = df['Order Date'] + pd.to_timedelta(np.random.randint(3, 8, n_records), unit='D')

# Add seasonality to sales (higher in Q4, lower in Q1)
df['month'] = df['Order Date'].dt.month
seasonal_multiplier = df['month'].map({
    1: 0.7, 2: 0.8, 3: 0.9, 4: 1.0, 5: 1.0, 6: 1.1,
    7: 1.1, 8: 1.2, 9: 1.1, 10: 1.3, 11: 1.5, 12: 1.6
})
df['Sales'] = df['Sales'] * seasonal_multiplier

# Calculate Profit (20-40% of Sales minus some based on discount)
df['Profit'] = df['Sales'] * (0.2 + np.random.uniform(0, 0.2, n_records)) - (df['Sales'] * df['Discount'] * 0.5)

# Remove temporary month column
df = df.drop('month', axis=1)

# Save to CSV in data folder
df.to_csv('data/superstore_sales.csv', index=False)

print(f"Sample Superstore dataset created with {len(df)} records")
print(f"Dataset saved to 'data/superstore_sales.csv'")
print(f"Date range: {df['Order Date'].min()} to {df['Order Date'].max()}")
print(f"Total Sales: ${df['Sales'].sum():,.2f}")
print("\nDataset structure:")
print(df.head())