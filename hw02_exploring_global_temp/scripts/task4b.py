from utils import load_and_group_data, configure_plot, handle_plot_output, set_labels
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    group_countries = load_and_group_data()
    configure_plot(use_ggplot=True)

    # b) to avoid too much of information split graphed data by Country
    palette = sns.color_palette(['black'])
    sns.lineplot(x="year", y="AverageTemperatureCelsius", data=group_countries, palette=palette, 
             hue='Country', legend=False)
    set_labels(xlabel='year', ylabel='countryAverage')
    plt.xticks([1800, 1900, 2000])

    handle_plot_output("task4b")

if __name__ == "__main__":
    main()