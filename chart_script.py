import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Create sample data since the CSV file is not available
# Generate dates from 2024-01-01 to 2025-03-31
start_date = pd.to_datetime('2024-01-01')
end_date = pd.to_datetime('2025-03-31')
dates = pd.date_range(start=start_date, end=end_date, freq='D')

# Create sample sales data with trend and seasonality
np.random.seed(42)
base_sales = 1000
trend = np.arange(len(dates)) * 0.5
seasonal = 100 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25)
noise = np.random.normal(0, 50, len(dates))
sales = base_sales + trend + seasonal + noise

# Add some uncertainty for forecast period
cutoff_date = pd.to_datetime('2024-12-31')
uncertainty = np.where(dates <= cutoff_date, 0, 
                      50 + (dates - cutoff_date).days.values * 0.2)

# Create DataFrame
df = pd.DataFrame({
    'ds': dates,
    'yhat': sales,
    'yhat_lower': sales - uncertainty - 30,
    'yhat_upper': sales + uncertainty + 30
})

# Split data into historical and forecast
historical = df[df['ds'] <= cutoff_date].copy()
forecast = df[df['ds'] > cutoff_date].copy()

# Create the figure
fig = go.Figure()

# Add historical data line
if not historical.empty:
    fig.add_trace(go.Scatter(
        x=historical['ds'],
        y=historical['yhat'],
        mode='lines',
        name='Historical',
        line=dict(color='#1FB8CD', width=2),
        cliponaxis=False
    ))

# Add forecast data line
if not forecast.empty:
    fig.add_trace(go.Scatter(
        x=forecast['ds'],
        y=forecast['yhat'],
        mode='lines',
        name='Forecast',  
        line=dict(color='#DB4545', width=2, dash='dash'),
        cliponaxis=False
    ))

# Add confidence interval shading for forecast period
if not forecast.empty:
    fig.add_trace(go.Scatter(
        x=pd.concat([forecast['ds'], forecast['ds'][::-1]]),
        y=pd.concat([forecast['yhat_upper'], forecast['yhat_lower'][::-1]]),
        fill='toself',
        fillcolor='rgba(219, 69, 69, 0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        name='Confidence',
        showlegend=True,
        cliponaxis=False
    ))

# Add vertical line to separate historical from forecast
fig.add_shape(
    type="line",
    x0=cutoff_date,
    y0=df['yhat'].min(),
    x1=cutoff_date,
    y1=df['yhat'].max(),
    line=dict(color="gray", width=1, dash="dot")
)

# Update layout
fig.update_layout(
    title='Daily Sales Forecast',
    xaxis_title='Date',
    yaxis_title='Sales',
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5)
)

# Save the chart
fig.write_image('daily_sales_forecast.png')