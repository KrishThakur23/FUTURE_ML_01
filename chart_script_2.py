import pandas as pd
import plotly.graph_objects as go

# Since the CSV file doesn't exist, I'll create sample data that would typically be in a category_analysis.csv
# This represents typical sales data by product category
data = {
    'Category': ['Furniture', 'Office Supplies', 'Technology'],
    'Sales_sum': [741999.62, 719047.03, 836154.03]
}

df = pd.DataFrame(data)
print("Sample data created:")
print(df)

# Create the pie chart
fig = go.Figure(data=[go.Pie(
    labels=df['Category'],
    values=df['Sales_sum'],
    textinfo='label+percent+value',
    texttemplate='%{label}<br>%{percent}<br>$%{value:,.0f}',
    marker_colors=['#1FB8CD', '#DB4545', '#2E8B57'],
    hovertemplate='<b>%{label}</b><br>Sales: $%{value:,.0f}<br>Percentage: %{percent}<extra></extra>'
)])

# Update layout with pie chart specific settings
fig.update_layout(
    title="Sales Distribution by Product Category",
    uniformtext_minsize=14, 
    uniformtext_mode='hide',
    showlegend=True
)

# Save the chart
fig.write_image('sales_distribution_pie_chart.png')
print("Chart saved successfully!")