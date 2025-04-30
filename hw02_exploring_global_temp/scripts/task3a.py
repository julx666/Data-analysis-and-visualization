from utils import load_and_sort_country_data, configure_plot, handle_plot_output, set_labels
import seaborn as sns

def main():
    df = load_and_sort_country_data()
    configure_plot(use_ggplot=True)

    # a) visualising the distribution of temperatures within each country
    sns.boxplot(x='country_id', y='AverageTemperatureCelsius', data=df, color= 'white', showcaps=False,
                 linecolor = "black", medianprops={"color": "black", 'linewidth': 2})

    set_labels(xlabel='country_id', ylabel='AverageTemperatureCelsius')

    handle_plot_output("task3a")

if __name__ == "__main__":
    main()