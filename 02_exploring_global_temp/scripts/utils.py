import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from typing import List, Dict

def load_data():
    """Load and return the temperature data (task 2)"""
    return pd.read_csv('../data/temperatures_clean.csv')

def load_and_sort_country_data():
    """Load and prepare country-sorted data (task 3)"""
    df = pd.read_csv('../data/temperatures_clean.csv')
    return df.sort_values('country_id')

def load_and_group_data():
    """Load and group country data (task 4 and 5a)"""
    df = pd.read_csv('../data/temperatures_clean.csv')
    group_countries = df.groupby(["year", "Country"])["AverageTemperatureCelsius"].mean().reset_index()
    sorted_countries = sorted(group_countries['Country'].unique())
    return group_countries, sorted_countries

def load_and_group_data_with_city():
    """Load and group country data (task 5b-5e)"""
    df = pd.read_csv('../data/temperatures_clean.csv')
    group_countries_cities = df.groupby(["year", "Country", "City"])["AverageTemperatureCelsius"].mean().reset_index()
    sorted_countries_cities = sorted(group_countries_cities["Country"].unique())
    return group_countries_cities, sorted_countries_cities

def configure_plot(use_ggplot=False):
    """Configure plot settings"""
    if use_ggplot:
        plt.style.use('ggplot')
    plt.figure(figsize=(10, 6))

def set_labels(xlabel, ylabel, fontweight='bold'):
    """Set axis labels with defaults."""
    plt.xlabel(xlabel, fontweight=fontweight)
    plt.ylabel(ylabel, fontweight=fontweight)

def handle_plot_output(plot_name):
    """Showing or saving the plot based on command line argument"""
    if len(sys.argv) > 1 and sys.argv[1] == '1':
        filename = f"{plot_name}.png"
        plt.savefig(filename, bbox_inches="tight")
        print(f"Plot saved to: {filename}")
    else:
        plt.show()

def setup_grid(num_items, ncols=3):
    """Set up a grid of subplots based on number of items"""
    nrows = (num_items + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(14, 8), sharex=True, sharey=True)

    # hide empty subplots
    for idx in range(num_items, nrows * ncols):
        axes.flat[idx].set_visible(False)
    
    return fig, axes, nrows, ncols

def set_subplots_labels(fig, xlabel, ylabel):
    """Set common x and y labels for subplots"""
    fig.text(0.5, 0.04, xlabel, ha='center', fontsize=18)
    fig.text(0.04, 0.5, ylabel, va='center', rotation='vertical', fontsize=18)

def set_subplot_properties(ax):
    """Set common properties for each subplot"""
    ax.set_xticks([1800, 1900, 2000])
    ax.set_yticks([-5, 0, 5, 10, 15, 20])
    ax.grid(True, alpha=0.3)

def add_legend(fig, handles, labels, title):
    """Add a legend to the figure"""
    fig.legend(handles=handles, 
              labels=labels, 
              title=title,
              loc='center right',
              bbox_to_anchor=(0.98, 0.5),
              fontsize=16,
              title_fontsize=16,
              frameon=False)
    plt.tight_layout(rect=[0, 0, 0.85, 0])
    plt.subplots_adjust(right=0.75, wspace=0.1, hspace=0.2)