
import pandas as pd
import numpy as np
from prophet import Prophet
import plotly.graph_objects as go
import plotly.express as px
import warnings
import os
from datetime import datetime

warnings.filterwarnings('ignore')

def create_folders():
    """Create required folder structure"""
    os.makedirs("data", exist_ok=True)
    os.makedirs("forecast", exist_ok=True)  
    os.makedirs("images", exist_ok=True)
    print("Folder structure created: data/, forecast/, images/")

def load_and_prepare_data():
    """Load and prepare data for forecasting"""
    print("Loading Superstore dataset...")
    df = pd.read_csv('data/superstore_sales.csv')
    df['Order Date'] = pd.to_datetime(df['Order Date'])

    # Aggregate daily sales
    daily_sales = df.groupby('Order Date').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum'
    }).reset_index()

    # Prepare for Prophet
    forecast_data = daily_sales.rename(columns={'Order Date': 'ds', 'Sales': 'y'})
    forecast_data = forecast_data.sort_values('ds').reset_index(drop=True)

    print(f"Data prepared: {len(forecast_data)} daily records")
    return df, forecast_data

def train_prophet_model(forecast_data):
    """Train Prophet forecasting model"""
    print("Training Prophet model...")
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False,
        seasonality_mode='multiplicative'
    )

    model.fit(forecast_data[['ds', 'y']])

    # Create 90-day forecast
    future = model.make_future_dataframe(periods=90, freq='D')
    forecast = model.predict(future)

    print("Forecasting completed (90 days ahead)")
    return model, forecast

def save_forecast_data(forecast, forecast_data):
    """Save forecast results to CSV files"""

    # Main daily forecast
    forecast_output = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
    forecast_output['ds'] = forecast_output['ds'].dt.strftime('%Y-%m-%d')
    forecast_output.to_csv('forecast/daily_forecast.csv', index=False)

    # Monthly forecast
    last_historical_date = forecast_data['ds'].max()
    future_forecast = forecast[forecast['ds'] > last_historical_date].copy()
    future_forecast['month'] = future_forecast['ds'].dt.month
    future_forecast['year'] = future_forecast['ds'].dt.year

    monthly_forecast = future_forecast.groupby(['year', 'month']).agg({
        'yhat': 'mean',
        'yhat_lower': 'mean', 
        'yhat_upper': 'mean'
    }).reset_index()

    month_names = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                   7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    monthly_forecast['month_name'] = monthly_forecast['month'].map(month_names)
    monthly_forecast.to_csv('forecast/monthly_forecast.csv', index=False)

    print("Forecast data saved to CSV files")

def create_analysis_files(df):
    """Create category and regional analysis files"""

    # Category analysis
    category_summary = df.groupby('Category').agg({
        'Sales': ['sum', 'mean'],
        'Profit': ['sum', 'mean'],
        'Quantity': ['sum', 'mean']
    }).round(2)

    category_summary.columns = ['_'.join(col).strip() for col in category_summary.columns]
    category_summary = category_summary.reset_index()
    category_summary.to_csv('forecast/category_analysis.csv', index=False)

    # Regional analysis
    regional_analysis = df.groupby('Region').agg({
        'Sales': ['sum', 'mean'],
        'Profit': ['sum', 'mean'],
        'Quantity': ['sum', 'mean']
    }).round(2)

    regional_analysis.columns = ['_'.join(col).strip() for col in regional_analysis.columns]
    regional_analysis = regional_analysis.reset_index()
    regional_analysis.to_csv('forecast/regional_analysis.csv', index=False)

    print("Analysis files created: category_analysis.csv, regional_analysis.csv")

def main():
    """Main execution function"""
    print("=== AI-Powered Sales Forecasting Dashboard ===")
    print("Starting forecasting pipeline...")

    # Step 1: Create folders
    create_folders()

    # Step 2: Load and prepare data
    df, forecast_data = load_and_prepare_data()

    # Step 3: Train model and forecast
    model, forecast = train_prophet_model(forecast_data)

    # Step 4: Save results
    save_forecast_data(forecast, forecast_data)
    create_analysis_files(df)

    # Step 5: Print summary
    total_sales = df['Sales'].sum()
    avg_daily_sales = forecast_data['y'].mean()
    future_90_days = forecast[forecast['ds'] > forecast_data['ds'].max()]['yhat'].sum()

    print("\n=== FORECASTING COMPLETE ===")
    print(f"Total Historical Sales: ${total_sales:,.2f}")
    print(f"Average Daily Sales: ${avg_daily_sales:,.2f}")
    print(f"90-Day Forecast Total: ${future_90_days:,.2f}")
    print("\nFiles created:")
    print("- forecast/daily_forecast.csv")
    print("- forecast/monthly_forecast.csv")
    print("- forecast/category_analysis.csv")
    print("- forecast/regional_analysis.csv")
    print("\nNext: Create charts and dashboard using the CSV files!")

if __name__ == "__main__":
    main()
