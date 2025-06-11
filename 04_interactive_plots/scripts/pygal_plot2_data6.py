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

custom_style = Style(
    stroke_width=5,
    dots_size=0.1,
    stroke_opacity=1,
    title_font_size=20,
    title_font_weight='bold',
    label_font_size=14,
    label_font_weight='bold',
    legend_font_size=12,
    plot_background = 'white',
    guide_stroke_dasharray='',
    major_guide_stroke_dasharray=''
)

# Plot data
plot = pygal.Line(
    title='Average Temperature Plot', 
    x_title='Year of Observation', 
    y_title='Average Temperature (°C)',
    show_legend=True,
    show_x_guides=True,
    show_y_guides=True,
    show_minor_x_labels=True,
    x_label_rotation=1,
    style=custom_style,
    include_x_axis=True
)

countries = df_size_reduced['Country'].unique()
# All unique years for x-axis labels
all_years = sorted(df_size_reduced['year'].unique())

# Set the x labels
plot.x_labels = [str(year) for year in all_years]
major_years = list(range(1750, 2001, 50))  # 1750, 1800, 1850, 1900, 1950, 2000
plot.x_labels_major = [str(year) for year in major_years]
plot.show_minor_x_labels = False  # Hide minor labels
plot.show_major_x_labels = True

# Add data series for each country
for country in countries:
    country_data = df_size_reduced[df_size_reduced['Country'] == country]
    
    # Create a dictionary mapping years to temperatures
    temp_dict = dict(zip(country_data['year'], country_data['AverageTemperatureCelsius']))
    
    # Create a list of values in the order of all_years (None if the year is missing)
    temperatures = [temp_dict.get(year) for year in all_years]
    plot.add(country, temperatures)

# Save the plot if argument is 1 or show if is 0
if len(sys.argv) > 1 and sys.argv[1] == '1':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    output_dir = os.path.join(project_root, 'plots')
    os.makedirs(output_dir, exist_ok=True)  # Create dir if missing

    filename = os.path.join(output_dir, "pygal_plot2_data6.png")  # Full path
    plot.render_to_png(filename=filename)
    print(f"Plot saved to: {os.path.abspath(filename)}")
else:
    plot.render_to_file('pygal_plot2_data6.svg')