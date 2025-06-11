import pandas as pd
import numpy as np
import sys
import os
import matplotlib.pyplot as plt
from statsmodels.tsa.api import VAR
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from sklearn.metrics import mean_absolute_error


# Load data
df = pd.read_csv('../data/temperatures_clean.csv')
countries = ['Brazil', 'Poland', 'Japan']

forecast_years = 200

df_grouped = df[df['Country'].isin(countries)].groupby(['year', 'Country'])['AverageTemperatureCelsius'].mean().reset_index()
df_wide = df_grouped.pivot(index='year', columns='Country', values='AverageTemperatureCelsius')
df_wide.index = pd.to_datetime(df_wide.index, format='%Y')
df_wide = df_wide.sort_index()

df_wide = df_wide.dropna()

# # Check stationarity (ADF test)
for country_name in countries:
    temp = df_wide[country_name]
    
    result = adfuller(temp)
    print(f"ADF statistic for {country_name}: {result[0]:.3f}, p-value: {result[1]:.3f}")

    # #ACF and PACF Plots
    # fig, ax = plt.subplots(2,1, figsize=(10,6))
    # plot_acf(temp, lags=30, ax=ax[0])
    # plot_pacf(temp, lags=30, ax=ax[1])
    # plt.tight_layout()
    # plt.show()

# Differencing to make data stationary
diff_data = df_wide.diff().dropna()  

# Fit the VAR model
model = VAR(diff_data)
results = model.fit(maxlags=15, ic='aic')  # Use AIC for lag selection

# Forecast the next 200 years
forecast_diff = results.forecast(diff_data.values[-results.k_ar:], steps=forecast_years)
forecast_diff_df = pd.DataFrame(forecast_diff, index=pd.date_range(df_wide.index[-1] + pd.DateOffset(1), periods=forecast_years, freq='Y'), columns=df_wide.columns)

# Reverse differencing to get actual forecast values
last_known = df_wide.iloc[-1]
forecast_values = forecast_diff_df.cumsum() + last_known

# Combine original and forecast for plotting
combined = pd.concat([df_wide, forecast_values])
combined.index.name = 'year'

for country in countries:
    country_id = df[df['Country'] == country]['country_id'].iloc[0]

    # Select the last 10 years of actual and forecasted data for the comparison
    actual_values = df_wide.iloc[-10:]  # Last 10 years
    forecasted_values = forecast_values.iloc[-10:]  # Last 10 years forecasted

    # Evaluating the model
    mae = mean_absolute_error(actual_values, forecasted_values)
    print(f'{country} - MAE: {mae:.3f}')
    
    # Plotting
    plt.figure(figsize=(14, 6))
    plt.plot(df_wide.index, df_wide[country], label='Observed')
    
    plt.plot(forecast_values.index, forecast_values[country], label='Forecast', color='red', linestyle='--')
    plt.title(f'{country} Temperature Forecast (200 Years)', fontsize=14, fontweight='bold')
    plt.xlabel('Year', fontsize=12, fontweight='bold')
    plt.ylabel('Average Temperature (°C)', fontsize=12, fontweight='bold')
    plt.legend()
    plt.grid(True)
    
    # Save the plot
    if len(sys.argv) > 1 and sys.argv[1] == '1':
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)

        output_dir = os.path.join(project_root, 'plots')
        os.makedirs(output_dir, exist_ok=True)  # Create dir if missing

        filename = os.path.join(output_dir, f'{country_id.lower()}_var.png')  # Full path
        plt.savefig(filename, dpi=300) 
        print(f"Plot saved to: {os.path.abspath(filename)}")  
    else:
        plt.show()