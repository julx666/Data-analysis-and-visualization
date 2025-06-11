from utils import load_data, configure_plot, handle_plot_output, set_labels
import matplotlib.pyplot as plt

def main():
    df = load_data()
    configure_plot(use_ggplot=False)  
    
    # a) first plot all AverageTemperatureCelsius vs. year
    plt.scatter(df['year'], df['AverageTemperatureCelsius'], 
                facecolors='none', edgecolors='black')
    
    set_labels(xlabel='temperature_complete', ylabel='AverageTemperatureCelsius')
    
    handle_plot_output("task2a")

if __name__ == "__main__":
    main()