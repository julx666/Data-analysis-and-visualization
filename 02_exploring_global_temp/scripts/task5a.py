from utils import load_and_group_data, handle_plot_output, setup_grid, set_subplots_labels, set_subplot_properties, add_legend
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    group_countries, sorted_countries = load_and_group_data()
    
    plt.style.use('ggplot')
    palette = sns.color_palette("husl", len(sorted_countries))

    fig, axes, nrows, ncols = setup_grid(len(sorted_countries))

    # Plot each country's data
    all_lines = []  # To store line objects for legend
    for idx, (ax, country) in enumerate(zip(axes.flat, sorted_countries)):
        country_data = group_countries[group_countries["Country"] == country]
        line = ax.plot(country_data["year"], country_data["AverageTemperatureCelsius"], 
                     color=palette[idx], label=country)
        all_lines.append(line[0])  # Store line object
        ax.set_title(country)
        set_subplot_properties(ax)

    set_subplots_labels(fig, 'year', 'countryAverage')
    add_legend(fig, all_lines, sorted_countries, 'Country')
    
    handle_plot_output("task5a")

if __name__ == "__main__":
    main()