import numpy as np
import pandas as pd
import sys
import os
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from sklearn.metrics import mean_absolute_error

# Load data
df = pd.read_csv('../data/temperatures_clean.csv')
countries = ['Brazil', 'Poland', 'Japan']

forecast_years = 200

for country_name in countries:
    country_df = df[df['Country'] == country_name]
    country_id = country_df['country_id'].iloc[0]
    
    # Calculate average temperature by year
    avg_temp = country_df.groupby('year')['AverageTemperatureCelsius'].mean().reset_index()
    
    # Format temperature and year
    avg_temp['year'] = pd.to_datetime(avg_temp["year"], format='%Y')
    avg_temp.set_index('year', inplace=True)
    temp = avg_temp['AverageTemperatureCelsius']
    
    # Check stationarity (ADF test)
    result = adfuller(temp)
    print(f"ADF statistic for {country_name}: {result[0]:.3f}, p-value: {result[1]:.3f}")
    
    # #ACF and PACF Plots
    # fig, ax = plt.subplots(2,1, figsize=(10,6))
    # plot_acf(temp, lags=30, ax=ax[0])
    # plot_pacf(temp, lags=30, ax=ax[1])
    # plt.tight_layout()
    # plt.show()

    # Define SARIMA parameters
    p, d, q = 1, 1, 1
    P, D, Q, s = 1, 1, 1, 36   

    # Fit the SARIMA model
    model = SARIMAX(temp, order=(p, d, q), seasonal_order=(P, D, Q, s))
    results = model.fit()

    # Forecast future
    last_year = temp.index[-1].year
    forecast_steps = forecast_years
    forecast = results.get_forecast(steps=forecast_steps)
    forecast_index = pd.date_range(start=f"{last_year+1}", periods=forecast_steps, freq='YS')
    forecast_mean = forecast.predicted_mean
    forecast_ci = forecast.conf_int()

    # Select the last 10 years of actual and forecasted data for the comparison
    actual_values = temp.iloc[-10:]  # Last 10 years
    forecasted_values = forecast_mean.iloc[-10:]  # Last 10 years forecasted

    # Evaluating the model
    mae = mean_absolute_error(actual_values, forecasted_values)
    print(f'{country_name} - MAE: {mae:.3f}')

    # Plotting
    plt.figure(figsize=(14, 6))
    plt.plot(temp.index, temp, label='Observed')

    plt.plot(forecast_index, forecast_mean, label='Forecast', color='red',  linestyle='--')

    plt.title(f"{country_name} Temperature Forecast (200 Years)", fontsize=14, fontweight='bold')
    plt.xlabel('Year', fontsize=12, fontweight='bold')
    plt.ylabel('Average Temperature (°C)', fontsize=12, fontweight='bold')

    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    # Save the plot
    if len(sys.argv) > 1 and sys.argv[1] == '1':
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)

        output_dir = os.path.join(project_root, 'plots')
        os.makedirs(output_dir, exist_ok=True)  # Create dir if missing

        filename = os.path.join(output_dir, f'{country_id.lower()}_sarima.png')  # Full path
        plt.savefig(filename, dpi=300) 
        print(f"Plot saved to: {os.path.abspath(filename)}")  
    else:
        plt.show()