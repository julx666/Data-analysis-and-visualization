import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.ticker as ticker


df = pd.read_csv('API_SP/API_SP.POP.TOTL_DS2_en_csv_v2_76253.csv', skiprows=4)
df_meta_data = pd.read_csv('API_SP/Metadata_Country_API_SP.POP.TOTL_DS2_en_csv_v2_76253.csv')

df_meta_data = df_meta_data.dropna(subset=['Region']) 
print(df_meta_data)

valid_country_codes = df_meta_data["Country Code"].unique()
df = df[df["Country Code"].isin(valid_country_codes)]

print(df)

# III) Exploration of the data.

def population_visualizations(df):
    # Get the year columns
    year_columns = [col for col in df.columns if col.isdigit()]
    countries_to_plot = ['Ukraine', 'Thailand', 'Iran, Islamic Rep.', 'Korea, Rep.']
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Get min and max populations across all years
    all_populations = []
    for year in year_columns:
        for country in countries_to_plot:
            population = df.loc[df['Country Name'] == country, year].values[0]
            all_populations.append(population)
    max_population = max(all_populations) * 1.2
    

    decline_year_idx = year_columns.index('1994')
    war_year_idx = year_columns.index('2021')
        
    # Create frame sequence with repeats for paused years
    frame_sequence = []
    for i in range(len(year_columns)):
        frame_sequence.append(i)
        if i == decline_year_idx or i == war_year_idx:
            frame_sequence.extend([i] * 50) # Add 50 extra frames
            
    # Find the index of the year 2021-2023 ("War Impact")
    war_year_idx = year_columns.index('2021')
    end_war_year_idx = year_columns.index('2023') 
        
    
    def animate(frame):
        year_idx = frame
        year = year_columns[year_idx]
        ax.clear()
        populations = []
        country_names = []
        
        for country in countries_to_plot:
            population = df.loc[df['Country Name'] == country, year].values[0]
            populations.append(population)
            country_names.append(country)
            
        default_color = 'blue'
        ukraine_color = 'crimson'

        # Colors list with same color for all countries initially
        colors = [default_color] * len(countries_to_plot)

        # Specify different color for Ukraine
        ukraine = countries_to_plot.index('Ukraine')
        colors[ukraine] = ukraine_color
        
        bars = ax.bar(country_names, populations, color=colors)
        ax.set_title('Population growth dynamics by year, compared to Ukraine', fontweight='bold', fontsize=18)
        ax.set_ylabel('Population [mln]', fontweight='bold', fontsize=14)
        ax.set_xlabel('Countries', fontweight='bold', fontsize=14)
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{x/1e6:.1f}'))
        
        # Set consistent y-axis limits
        ax.set_ylim(0, max_population)
        
        # Year text
        ax.text(0.05, 0.9, f'{year}',
                transform=ax.transAxes, fontsize=16, fontweight='bold')
        
        # Add bar labels
        for population, bar in zip(populations, bars):
            height = bar.get_height()
            label = f'{population / 1e6:.1f}M'
            ax.text(bar.get_x() + bar.get_width() / 2.0, height + 0.01 * max_population,
                    label, ha='center', va='bottom', fontweight='bold')
        
        # Add decline year text
        if year_idx == decline_year_idx:
            ax.text(0.05, 0.85, 'Desintegration of Soviet Union',
                   transform=ax.transAxes, fontsize=16, fontweight='bold', color='crimson')
            ax.axhline(y=52.1*1e6, color='r', linestyle='--')
        
        # Add war year text
        if war_year_idx is not None and end_war_year_idx is not None and war_year_idx <= year_idx <= end_war_year_idx:
            ax.text(0.05, 0.85, 'War Impact',
                   transform=ax.transAxes, fontsize=16, fontweight='bold', color='crimson')
        if year_idx == war_year_idx:
            ax.axhline(y=44.3*1e6, color='r', linestyle='--')
    
    # Create animation
    ani = FuncAnimation(fig, animate, frames=frame_sequence, interval=150, repeat=True)
    ani.save('Population_growth.gif', writer='Pillow')
    
    plt.tight_layout()
    plt.show()

population_visualizations(df)