# AI-Powered Sales Forecasting Dashboard

This project creates a comprehensive sales forecasting dashboard using the Superstore dataset, Facebook Prophet for time series forecasting, and interactive visualizations.

## Project Structure

```
project/
├── data/
│   └── superstore_sales.csv          # Raw dataset
├── forecast/
│   ├── daily_forecast.csv            # Daily forecast with confidence intervals
│   ├── monthly_forecast.csv          # Monthly aggregated forecasts
│   ├── category_analysis.csv         # Category-wise sales analysis
│   └── regional_analysis.csv         # Regional sales analysis
├── images/
│   ├── daily_sales_forecast.png      # Line chart: Historical vs Predicted
│   ├── monthly_sales_forecast.png    # Bar chart: Monthly forecasts
│   └── sales_distribution_pie_chart.png # Pie chart: Category distribution
└── sales_forecasting_script.py       # Main forecasting script
```

## Requirements

Install required packages:

```bash
pip install pandas numpy prophet plotly kaleido matplotlib
```

## How to Run

1. **Prepare your data**: Place your Superstore dataset CSV file in the `data/` folder as `superstore_sales.csv`

2. **Run the forecasting script**:
```bash
python sales_forecasting_script.py
```

This will:
- Create the folder structure
- Load and process the Superstore data
- Train a Prophet forecasting model
- Generate 90-day sales forecasts
- Save all results as CSV files
- Create analysis files for categories and regions

3. **View the dashboard**: run python -m http.server 8000 on terminal then open localhost:8000

## What You'll Get

### Forecasting Model
- **Facebook Prophet** time series model with seasonal components
- **90-day forecast** with confidence intervals
- **Historical trend analysis** and pattern detection

### Visualizations
- **Line Chart**: Daily sales history vs predictions
- **Bar Chart**: Monthly forecast breakdown
- **Pie Chart**: Sales distribution by product category

### Business Analytics
- **KPI Dashboard** with key metrics
- **Category Analysis** (Furniture, Office Supplies, Technology)
- **Regional Performance** breakdown
- **Business Recommendations** based on forecast insights

### CSV Outputs
All forecast data and analysis results are saved as CSV files for further analysis or integration with other tools.

## Business Value

This dashboard helps retail businesses:
- **Predict future sales** with statistical confidence
- **Plan inventory** based on seasonal patterns
- **Identify growth opportunities** by category and region
- **Make data-driven decisions** for marketing and operations
- **Monitor model performance** with accuracy metrics

## Key Features

- ✅ **Proper folder organization** (data/, forecast/, images/)
- ✅ **Multiple chart types** (line, bar, pie)
- ✅ **Interactive dashboard**
- ✅ **Business insights** and recommendations
- ✅ **Professional visualizations** with confidence intervals
- ✅ **Scalable codebase** for different datasets

## Customization

You can modify the forecasting script to:
- Change forecast horizon (currently 90 days)
- Adjust Prophet model parameters
- Add custom holidays or events
- Create additional visualizations
- Export results in different formats

This project demonstrates real-world business intelligence and predictive analytics skills suitable for consulting, analytics, and retail SaaS applications.
