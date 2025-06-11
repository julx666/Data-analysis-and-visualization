from utils import load_and_sort_country_data, configure_plot, handle_plot_output, set_labels
import seaborn as sns

def main():
    df = load_and_sort_country_data()
    configure_plot(use_ggplot=True)

    # b) add jitter to boxplot
    sns.stripplot(x='country_id', y='AverageTemperatureCelsius', data=df, color='red', jitter=0.4, alpha=0.1)
    sns.boxplot(x='country_id', y='AverageTemperatureCelsius', data=df, color= 'white', linewidth = 2, showcaps=False, linecolor = "black",
             medianprops={"color": "black", 'linewidth': 2}, zorder=3)

    set_labels(xlabel='country_id', ylabel='AverageTemperatureCelsius')

    handle_plot_output("task3b")

if __name__ == "__main__":
    main()
