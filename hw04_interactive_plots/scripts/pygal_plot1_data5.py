import pandas as pd
from pygal.style import Style
import pygal
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

custom_style = Style(dots_size=20,
              title_font_size=20,
              title_font_weight='bold',
              label_font_size=14,   
              label_font_weight='bold',  
              legend_font_size=12,
              guide_stroke_dasharray='',
              major_guide_stroke_dasharray=''
            )

# Plot data
plot = pygal.XY(title='Average Temperature Plot', x_title='Year of Observation', y_title='Average Temperature (°C)', 
                show_legend=True,
                show_x_guides=True,
                show_y_guides=True,
                style=custom_style)

for country in df_size_reduced['Country'].unique():
    country_data = df_size_reduced[df_size_reduced['Country'] == country]
    points = [(row['year'], row['AverageTemperatureCelsius'], {'label': f'{country}'}) for _, row in country_data.iterrows()]
    plot.add(country, points, stroke=False)

# Save the plot if argument is 1 or show if is 0
if len(sys.argv) > 1 and sys.argv[1] == '1':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    output_dir = os.path.join(project_root, 'plots')
    os.makedirs(output_dir, exist_ok=True) # Create dir if missing

    filename = os.path.join(output_dir, "pygal_plot1_data5.png") # Full path
    plot.render_to_png(filename=filename)
    print(f"Plot saved to: {os.path.abspath(filename)}")
else:
    plot.render_to_file('pygal_plot1_data5.svg')
