# Load the dataset and prepare for forecasting
df = pd.read_csv('data/superstore_sales.csv')

# Convert Order Date to datetime
df['Order Date'] = pd.to_datetime(df['Order Date'])

print("Data loaded successfully!")
print(f"Dataset shape: {df.shape}")
print(f"Date range: {df['Order Date'].min()} to {df['Order Date'].max()}")

# Aggregate sales by date for time series forecasting
daily_sales = df.groupby('Order Date').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Quantity': 'sum'
}).reset_index()

# Prepare data for Prophet (requires 'ds' and 'y' columns)
forecast_data = daily_sales.rename(columns={'Order Date': 'ds', 'Sales': 'y'})
forecast_data = forecast_data.sort_values('ds').reset_index(drop=True)

print(f"Daily aggregated data shape: {forecast_data.shape}")
print("Sample of daily sales data:")
print(forecast_data.head())

# Create and train Prophet model
model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False,
    seasonality_mode='multiplicative'
)

# Fit the model
model.fit(forecast_data[['ds', 'y']])

# Create future dataframe for 90 days forecast
future = model.make_future_dataframe(periods=90, freq='D')
forecast = model.predict(future)

print(f"Forecast completed for {len(future)} days (including historical + 90 future days)")

# Save main forecast data to CSV
forecast_output = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
forecast_output['ds'] = forecast_output['ds'].dt.strftime('%Y-%m-%d')
forecast_output.to_csv('forecast/daily_forecast.csv', index=False)

print("Daily forecast saved to 'forecast/daily_forecast.csv'")
print(forecast_output.tail())