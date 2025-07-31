
import pandas as pd
import numpy as np
from prophet import Prophet
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

print("Loading Sample Superstore dataset...")

# Load the dataset
df = pd.read_csv('sample_superstore.csv')
df['Order Date'] = pd.to_datetime(df['Order Date'])

print(f"Dataset loaded: {len(df)} records from {df['Order Date'].min()} to {df['Order Date'].max()}")

# Aggregate daily sales
daily_sales = df.groupby('Order Date').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Quantity': 'sum'
}).reset_index()

# Prepare data for Prophet (requires 'ds' and 'y' columns)
prophet_data = daily_sales[['Order Date', 'Sales']].copy()
prophet_data.columns = ['ds', 'y']
prophet_data = prophet_data.sort_values('ds')

print(f"Daily sales data prepared: {len(prophet_data)} days")
print(f"Average daily sales: ${prophet_data['y'].mean():.2f}")

# Initialize and train Prophet model
print("Training Prophet forecasting model...")
model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False,
    seasonality_mode='multiplicative',
    changepoint_prior_scale=0.05
)

# Add US holidays
model.add_country_holidays(country_name='US')

# Fit the model
model.fit(prophet_data)

# Create future dataframe for next 90 days
future = model.make_future_dataframe(periods=90, freq='D')
print(f"Generating forecasts for next 90 days...")

# Generate forecasts
forecast = model.predict(future)

# Calculate model accuracy metrics
historical_forecast = forecast[forecast['ds'] <= prophet_data['ds'].max()].copy()
historical_actual = prophet_data.copy()

# Merge for comparison
comparison = historical_actual.merge(historical_forecast[['ds', 'yhat']], on='ds')
comparison['error'] = comparison['y'] - comparison['yhat']
comparison['abs_error'] = abs(comparison['error'])
comparison['pct_error'] = abs(comparison['error']) / comparison['y'] * 100

mae = comparison['abs_error'].mean()
mape = comparison['pct_error'].mean()

print(f"Model Accuracy Metrics:")
print(f"  Mean Absolute Error (MAE): ${mae:.2f}")
print(f"  Mean Absolute Percentage Error (MAPE): {mape:.1f}%")

# Prepare forecast data for export
forecast_export = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
forecast_export['ds'] = forecast_export['ds'].dt.strftime('%Y-%m-%d')
forecast_export['yhat'] = forecast_export['yhat'].round(2)
forecast_export['yhat_lower'] = forecast_export['yhat_lower'].round(2)
forecast_export['yhat_upper'] = forecast_export['yhat_upper'].round(2)

# Add actual sales where available
forecast_export = forecast_export.merge(
    prophet_data.rename(columns={'ds': 'ds_temp', 'y': 'actual_sales'}),
    left_on='ds', right_on='ds_temp', how='left'
).drop('ds_temp', axis=1)

# Save full forecast data to CSV
forecast_export.to_csv('forecast_data.csv', index=False)
print("Full forecast data saved to 'forecast_data.csv'")

# Generate monthly forecasts
forecast['month'] = forecast['ds'].dt.month
forecast['year'] = forecast['ds'].dt.year
forecast['month_year'] = forecast['ds'].dt.to_period('M')

# Get future dates only for monthly summary
future_forecast = forecast[forecast['ds'] > prophet_data['ds'].max()].copy()

monthly_forecast = future_forecast.groupby(['year', 'month']).agg({
    'yhat': 'mean',
    'yhat_lower': 'mean', 
    'yhat_upper': 'mean'
}).reset_index()

# Add month names
import calendar
monthly_forecast['month_name'] = monthly_forecast['month'].apply(lambda x: calendar.month_abbr[x])
monthly_forecast['yhat'] = monthly_forecast['yhat'].round(2)
monthly_forecast['yhat_lower'] = monthly_forecast['yhat_lower'].round(2)
monthly_forecast['yhat_upper'] = monthly_forecast['yhat_upper'].round(2)

# Save monthly forecast
monthly_forecast.to_csv('monthly_forecast.csv', index=False)
print("Monthly forecast data saved to 'monthly_forecast.csv'")

# Create category-wise forecasts
print("Generating category-wise forecasts...")
category_forecasts = {}

for category in df['Category'].unique():
    cat_data = df[df['Category'] == category].copy()
    cat_daily = cat_data.groupby('Order Date')['Sales'].sum().reset_index()
    cat_daily.columns = ['ds', 'y']

    if len(cat_daily) > 30:  # Only forecast if we have sufficient data
        cat_model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=False,
            seasonality_mode='multiplicative'
        )
        cat_model.fit(cat_daily)
        cat_future = cat_model.make_future_dataframe(periods=90, freq='D')
        cat_forecast = cat_model.predict(cat_future)

        category_forecasts[category] = cat_forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()

# Save category forecasts
for category, cat_forecast in category_forecasts.items():
    filename = f'forecast_{category.lower().replace(" ", "_")}.csv'
    cat_forecast['ds'] = cat_forecast['ds'].dt.strftime('%Y-%m-%d')
    cat_forecast.to_csv(filename, index=False)
    print(f"Category forecast saved: {filename}")

# Generate summary statistics
summary_stats = {
    'total_historical_days': len(prophet_data),
    'forecast_days': 90,
    'avg_daily_sales': prophet_data['y'].mean(),
    'total_historical_sales': prophet_data['y'].sum(),
    'predicted_90_day_sales': future_forecast['yhat'].sum(),
    'model_mae': mae,
    'model_mape': mape,
    'categories_forecasted': list(category_forecasts.keys())
}

# Save summary
import json
with open('forecast_summary.json', 'w') as f:
    json.dump(summary_stats, f, indent=2, default=str)

print("\nForecast Summary:")
print(f"  Historical period: {len(prophet_data)} days")
print(f"  Average daily sales: ${summary_stats['avg_daily_sales']:.2f}")
print(f"  Total historical sales: ${summary_stats['total_historical_sales']:,.2f}")
print(f"  Predicted 90-day sales: ${summary_stats['predicted_90_day_sales']:,.2f}")
print(f"  Categories forecasted: {len(category_forecasts)}")

print("\nAll forecast files generated successfully!")
print("Files created:")
print("  - forecast_data.csv (daily forecasts)")
print("  - monthly_forecast.csv (monthly averages)")
for category in category_forecasts.keys():
    print(f"  - forecast_{category.lower().replace(' ', '_')}.csv")
print("  - forecast_summary.json")

