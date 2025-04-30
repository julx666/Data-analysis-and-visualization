from utils import load_and_group_data, configure_plot, handle_plot_output, set_labels
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    group_countries, sorted_countries = load_and_group_data()
    configure_plot(use_ggplot=True)

    # c) and add color
    plot = sns.lineplot(x="year", y="AverageTemperatureCelsius", data=group_countries, hue='Country', hue_order=sorted_countries)
    legend = plt.legend(title= 'Country', loc= "center left", bbox_to_anchor=(1, 0.5), frameon=False) 
    legend_title = legend.get_title()
    legend_title.set_weight('bold')
   
    set_labels(xlabel='year', ylabel='countryAverage')
    plt.xticks([1800, 1900, 2000])
    plt.tight_layout()

    handle_plot_output("task4c")

if __name__ == "__main__":
    main()