from utils import load_and_group_data_with_city, handle_plot_output, setup_grid, set_subplots_labels, set_subplot_properties, add_legend
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    group_countries_cities, sorted_countries = load_and_group_data_with_city()
    
    # Sort cities in alphabetical order and add unique color to each
    sorted_cities = sorted(group_countries_cities["City"].unique())
    palette = sns.color_palette("husl", len(sorted_cities))
    city_colors = {city: palette[i] for i, city in enumerate(sorted_cities)}

    fig, axes, nrows, ncols = setup_grid(len(sorted_countries))

    # Plot each country's data
    all_lines = [] 
    for idx, (ax, country) in enumerate(zip(axes.flat, sorted_countries)):
        country_data = group_countries_cities[group_countries_cities["Country"] == country]
        cities = sorted(country_data['City'].unique())

        for city in cities:
            city_data = country_data[country_data['City'] == city]
            line = ax.plot(city_data["year"], city_data["AverageTemperatureCelsius"], 
                        color=city_colors[city], label=city)
            all_lines.append(line[0])
        ax.set_title(country)
        set_subplot_properties(ax)

    set_subplots_labels(fig, 'year', 'cityAverage')
    add_legend(fig, all_lines, sorted_cities, 'City')
    
    handle_plot_output("task5d")

if __name__ == "__main__":
    main()