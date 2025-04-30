import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import mpld3
import sys
import os

# Load data
df = pd.read_csv('../data/temperatures_clean.csv')

# Group by country and decade
df_size_reduced = df.groupby(
    ['Country', (df['year'] // 10 * 10).rename('decade')]
).agg({
    'AverageTemperatureCelsius': 'mean',
    'year': 'first'  # Keep the first year of each decade
}).reset_index()

# Create figure
fig, ax = plt.subplots(figsize=(10, 6))

# Format x-axis to avoid commas in year numbers
ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:.0f}'))

# Plot data
interactive_points = []
countries = df_size_reduced['Country'].unique()
colors = plt.cm.get_cmap('tab10', len(countries))

for i, country in enumerate(countries):
    country_data = df_size_reduced[df_size_reduced['Country'] == country]
    
    # Plot the line 
    line = ax.plot(
        country_data['year'],
        country_data['AverageTemperatureCelsius'],
        color=colors(i),
        label=country,
        linewidth=10,
        alpha=0.7
    )
    
    # Invisible scatter points for interactivity
    scatter = ax.scatter(
        country_data['year'],
        country_data['AverageTemperatureCelsius'],
        color=colors(i),
        alpha=0,  
        edgecolors='none'
    )
    
    # Create tooltip labels
    labels = [
        f"{row['Country']} ({int(row['year'])}): {row['AverageTemperatureCelsius']:.2f}°C"
        for _, row in country_data.iterrows()
    ]
    
    # Store for later use with plugins
    interactive_points.append((scatter, labels))

# Style the plot
ax.set_title('Average Temperature Plot', fontsize=25, fontweight='bold')
ax.set_xlabel('Year of Observation', fontsize=18, fontweight='bold')
ax.set_ylabel('Average Temperature (°C)', fontsize=18, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.legend(
    title='Country',
    title_fontsize=18,
    fontsize=14,
    bbox_to_anchor=(1, 0.9),
    loc='upper left'
)

plt.tight_layout()

# Connect tooltips to the figure
for scatter, labels in interactive_points:
    tooltip = mpld3.plugins.PointLabelTooltip(scatter, labels=labels)
    mpld3.plugins.connect(fig, tooltip)

# Save the plot if argument is 1 or show if is 0
if len(sys.argv) > 1 and sys.argv[1] == '1':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    output_dir = os.path.join(project_root, 'plots')
    os.makedirs(output_dir, exist_ok=True) # Create dir if missing
    
    filename = os.path.join(output_dir, "mpld3_plot2_data4.png") # Full path
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Plot saved to: {os.path.abspath(filename)}")
else:
    mpld3.show()