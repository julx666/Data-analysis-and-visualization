import pandas as pd
import matplotlib.pyplot as plt
import os
import sys


# Load data
df =  pd.read_csv('../data/temperatures_clean.csv')
countries = df['Country'].unique()

for country in countries:
    country_data = df[df['Country'] == country]
    country_id = country_data['country_id'].iloc[0]
    # Group by year and compute average temperature
    avg_temp = country_data.groupby('year')['AverageTemperatureCelsius'].mean().reset_index()

    # Plotting
    plt.figure(figsize=(10,6))
    plt.scatter(avg_temp['year'], avg_temp['AverageTemperatureCelsius'], s=10)  
    plt.title(f'Average Temperature for: {country}', fontsize=14, fontweight='bold')
    plt.xlabel('Year', fontweight='bold')
    plt.ylabel('Average Temperature (°C)', fontweight='bold')
    plt.xlim(1800, 2000)
    plt.grid(True, alpha=0.3)

    # Save the plot
    if len(sys.argv) > 1 and sys.argv[1] == '1':
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)

        output_dir = os.path.join(project_root, 'plots')
        os.makedirs(output_dir, exist_ok=True)  # Create dir if missing

        filename = os.path.join(output_dir, f'{country_id.lower()}.png')  # Full path
        plt.savefig(filename, dpi=300) 
        print(f"Plot saved to: {os.path.abspath(filename)}")  
    else:
        plt.show()