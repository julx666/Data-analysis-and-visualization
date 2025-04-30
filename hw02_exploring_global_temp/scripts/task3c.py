from utils import load_and_sort_country_data, configure_plot, handle_plot_output, set_labels
import seaborn as sns

def main():
    df = load_and_sort_country_data()
    configure_plot(use_ggplot=True)

    # c) change boxplot to violin plot
    color = sns.color_palette("pastel", n_colors=len(df['country_id']))
    sns.violinplot(x='country_id', y='AverageTemperatureCelsius', data=df, palette=color)

    set_labels(xlabel='country_id', ylabel='AverageTemperatureCelsius')

    handle_plot_output("task3c")

if __name__ == "__main__":
    main()