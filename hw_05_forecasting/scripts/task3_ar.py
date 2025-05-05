import pandas as pd
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.ar_model import AutoReg, ar_select_order
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
    
    # Create differenced series for stationarity
    temp_diff = temp.diff().dropna()
    
    # #ACF and PACF Plots
    # fig, ax = plt.subplots(2,1, figsize=(10,6))
    # plot_acf(temp_diff, lags=30, ax=ax[0])
    # plot_pacf(temp_diff, lags=30, ax=ax[1])
    # plt.tight_layout()
    # plt.show()
    
    # Split the dataset
    n = len(temp_diff)
    train_end = int(n * 0.8)
    train = temp_diff.iloc[:train_end]
    test = temp_diff.iloc[train_end:]
    
    # Model Fitting
    sel = ar_select_order(train, maxlag=30, ic='aic', old_names=False)
    best_p = sel.ar_lags
    if best_p is None or len(best_p) == 0:
        best_p = 1
    else:
        best_p = best_p[-1]

    # Fit the AutoReg model           
    model = AutoReg(train, lags=best_p, old_names=False)
    model_fit = model.fit()
    
    pred_test = model_fit.predict(start=train_end, end=n-1, dynamic=False)

    # Evaluating the model
    mae = mean_absolute_error(test, pred_test)
    print(f'{country_name} - MAE: {mae:.3f}')

   # Forecasting future years
    full_model = AutoReg(temp_diff, lags=best_p, old_names=False).fit()
    future_pred_diff = full_model.predict(start=n, end=n + forecast_years - 1, dynamic=False)
    
   # Undo differencing to get temperature predictions
    last_actual_temp = temp.iloc[-1]
    future_temp = future_pred_diff.cumsum() + last_actual_temp
    
    # Prepare future years for plotting
    future_years = pd.date_range(start=temp.index[-1] + pd.DateOffset(years=1), periods=forecast_years, freq='YS')
    future_temp.index = future_years
    
    # Plotting
    plt.figure(figsize=(14, 6))
    plt.plot(temp.index, temp, label='Observed temperatures', linewidth=2)

    plt.plot(future_temp.index, future_temp, label='Forecast temperatures', linestyle='--', linewidth=2, color='red')

    plt.title(f'{country_name} Temperature Forecast (200 years)', fontsize=14, fontweight='bold')
    plt.xlabel('Year', fontsize=12, fontweight='bold')
    plt.ylabel('Average Temperature (°C)', fontsize=12, fontweight='bold')

    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save the plot
    if len(sys.argv) > 1 and sys.argv[1] == '1':
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)

        output_dir = os.path.join(project_root, 'plots')
        os.makedirs(output_dir, exist_ok=True)  # Create dir if missing

        filename = os.path.join(output_dir, f'{country_id.lower()}_ar.png')  # Full path
        plt.savefig(filename, dpi=300) 
        print(f"Plot saved to: {os.path.abspath(filename)}")  
    else:
        plt.show()