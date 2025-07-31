# Create monthly forecast summary
forecast['month'] = forecast['ds'].dt.month
forecast['year'] = forecast['ds'].dt.year
forecast['month_year'] = forecast['ds'].dt.to_period('M')

# Get only future forecasts (after the last historical date)
last_historical_date = forecast_data['ds'].max()
future_forecast = forecast[forecast['ds'] > last_historical_date].copy()

# Monthly aggregation of forecasts
monthly_forecast = future_forecast.groupby(['year', 'month']).agg({
    'yhat': 'mean',
    'yhat_lower': 'mean', 
    'yhat_upper': 'mean'
}).reset_index()

# Add month names
month_names = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
               7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
monthly_forecast['month_name'] = monthly_forecast['month'].map(month_names)
monthly_forecast['period'] = monthly_forecast['year'].astype(str) + '-' + monthly_forecast['month_name']

# Save monthly forecast
monthly_forecast.to_csv('forecast/monthly_forecast.csv', index=False)

print("Monthly forecast saved to 'forecast/monthly_forecast.csv'")
print(monthly_forecast)

# Create category-wise historical analysis and simple forecast
category_sales = df.groupby(['Category', df['Order Date'].dt.to_period('M')]).agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Quantity': 'sum'
}).reset_index()

category_sales['Order Date'] = category_sales['Order Date'].dt.to_timestamp()

# Save category analysis
category_summary = df.groupby('Category').agg({
    'Sales': ['sum', 'mean'],
    'Profit': ['sum', 'mean'],
    'Quantity': ['sum', 'mean']
}).round(2)

# Flatten column names
category_summary.columns = ['_'.join(col).strip() for col in category_summary.columns]
category_summary = category_summary.reset_index()
category_summary.to_csv('forecast/category_analysis.csv', index=False)

print("\nCategory analysis saved to 'forecast/category_analysis.csv'")
print(category_summary)

# Create regional analysis
regional_analysis = df.groupby('Region').agg({
    'Sales': ['sum', 'mean'],
    'Profit': ['sum', 'mean'],
    'Quantity': ['sum', 'mean']
}).round(2)

regional_analysis.columns = ['_'.join(col).strip() for col in regional_analysis.columns]
regional_analysis = regional_analysis.reset_index()
regional_analysis.to_csv('forecast/regional_analysis.csv', index=False)

print("\nRegional analysis saved to 'forecast/regional_analysis.csv'")
print(regional_analysis)