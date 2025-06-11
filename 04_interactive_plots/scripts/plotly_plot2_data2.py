import pandas as pd
import plotly.express as px
import os
import sys

# Load data
df = pd.read_csv('../data/temperatures_clean.csv')

# Group by country and decade
df_size_reduced = df.groupby(
    ['Country', (df['year'] // 10 * 10).rename('decade')]  # Group by decade
).agg({
    'AverageTemperatureCelsius': 'mean', 
    'year': 'first'  # Keep the first year of each decade 
}).reset_index()

# Plot data
fig = px.line(df_size_reduced, x="year", y="AverageTemperatureCelsius", color="Country", symbol="Country")

fig.update_layout(
    title_text='Average Temperature Plot',
    title_font=dict(size=35, weight='bold'),
    title={
        'y':0.95,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'}
)
fig.update_xaxes(
    title_text='Year of Observation',
    title_font=dict(size=20, weight='bold'),
    mirror=True,
    ticks='outside',
    showline=True,
    linecolor='black',
    gridcolor='lightgrey'
)
fig.update_yaxes(
    title_text='Average Temperature (°C)',
    title_font=dict(size=20, weight='bold'),
    mirror=True,
    ticks='outside',
    showline=True,
    linecolor='black',
    gridcolor='lightgrey'
)
fig.update_layout(
    legend=dict(
        title=dict(font=dict(size=25, weight='bold')) 
    )
)
fig.update_layout(
    legend=dict(
        font=dict(size=20)  
    )
)
fig.update_layout(
    margin=dict(l=50, r=50, t=100, b=50),  # Increase top margin for title
    autosize=False,
    width=1200,  # Adjust width
    height=800,   # Adjust height
    plot_bgcolor='white'
)
fig.update_traces(marker=dict(size=1),
                  line=dict(width=4))

# Save the plot if argument is 1 or show if is 0
if len(sys.argv) > 1 and sys.argv[1] == '1':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    output_dir = os.path.join(project_root, 'plots')
    os.makedirs(output_dir, exist_ok=True)  # Create dir if missing

    filename = os.path.join(output_dir, "plotly_plot2_data2.png")  # Full path
    fig.write_image(filename, scale=2)  
    print(f"Plot saved to: {os.path.abspath(filename)}")  
else:
    fig.show()
