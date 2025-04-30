from utils import load_and_group_data, configure_plot, handle_plot_output, set_labels
import matplotlib.pyplot as plt

def main():
    group_countries = load_and_group_data()
    configure_plot(use_ggplot=True)

    # a) calculate average temperature per year per each country 
    plt.plot(group_countries["year"], group_countries["AverageTemperatureCelsius"], color="black")
    set_labels(xlabel='year', ylabel='countryAverage')
    plt.xticks([1800, 1900, 2000])

    handle_plot_output("task4a")

if __name__ == "__main__":
    main()