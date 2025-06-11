from utils import load_data, configure_plot, handle_plot_output, set_labels
import matplotlib.pyplot as plt

def main():
    df = load_data()
    configure_plot(use_ggplot=True)  
    
    # b) recreate the plot using 'points' instead 'circles', add grid
    plt.scatter(df['year'], df['AverageTemperatureCelsius'], color='black')
    plt.grid(True, color='white', linestyle='-', linewidth=0.5)
    
    set_labels(xlabel='temperature_complete', ylabel='AverageTemperatureCelsius')
    
    handle_plot_output("task2b")

if __name__ == "__main__":
    main()