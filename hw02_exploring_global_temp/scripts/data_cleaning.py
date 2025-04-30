import pandas as pd

df = pd.read_csv("temperature.csv", sep=',')

# a) there are missing values for City and Country in some records, remove those
df = df.dropna(subset=['City', 'Country'])
# b) there are NA's in AverageTemperatureFahr and AverageTemperatureUncertaintyFahr, 
#remove rows with missing values in those fields
df = df.dropna(subset=['AverageTemperatureFahr', 'AverageTemperatureUncertaintyFahr'])
#c) remove empty 'City' and 'Country' fields
df = df[(df['City'] != "") & (df['Country'] != "")]
#d) 'day' field has no other values besides 1, thus you can remove it from the data
df = df.drop(columns='day', axis=1)
# e) convert AverageTemperatureFahr and AverageTemperatureUncertaintyFahr into 
# AverageTemperatureCelsius and AverageTemperatureUncertaintyCelsius 
# Convert Fahrenheit to Celsius
df['AverageTemperatureCelsius'] = (df['AverageTemperatureFahr'] - 32) * (5 / 9)
df['AverageTemperatureUncertaintyCelsius'] = (df['AverageTemperatureUncertaintyFahr'] - 32) * (5 / 9)

# Drop the Fahrenheit columns
df = df.drop(columns=['AverageTemperatureFahr', 'AverageTemperatureUncertaintyFahr'])

df.to_csv('temperatures_clean.csv', index=False)

