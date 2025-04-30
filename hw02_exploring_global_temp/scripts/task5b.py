from utils import load_and_group_data_with_city, handle_plot_output, setup_grid, set_subplots_labels, set_subplot_properties, add_legend
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    group_countries_cities, sorted_countries_cities = load_and_group_data_with_city()
    
    plt.style.use('ggplot')
    palette = sns.color_palette("husl", len(sorted_countries_cities))

    fig, axes, nrows, ncols = setup_grid(len(sorted_countries_cities))

    # Plot each country's data
    all_lines = [] 
    for idx, (ax, country) in enumerate(zip(axes.flat, sorted_countries_cities)):
        country_data = group_countries_cities[group_countries_cities["Country"] == country]
        cities = country_data['City'].unique()

        for city in cities:
            city_data = country_data[country_data['City'] == city]
            line = ax.plot(city_data["year"], city_data["AverageTemperatureCelsius"], 
                        color=palette[idx], label=city)
            all_lines.append(line[0])
        ax.set_title(country)

    set_subplots_labels(fig, 'year', 'cityAverage')
    add_legend(fig, all_lines, sorted_countries_cities, 'Country')
    
    handle_plot_output("task5b")

if __name__ == "__main__":
    main()