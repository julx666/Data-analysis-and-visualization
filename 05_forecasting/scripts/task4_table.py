import pandas as pd

def create_comparison_table():
    # MAE results data 
    data = {
        'Country': ['Brazil', 'Poland', 'Japan'],
        'AR': [0.301, 0.733, 0.676],   
        'ARIMA': [0.291, 0.743, 0.650],     
        'SARIMA': [1.460, 1.612, 1.395],
        'VAR': [1.428, 1.428, 1.428]        
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Format the table with borders
    border = '-' * 40
    header = f"{'Country':<10} {'AR':<8} {'ARIMA':<8} {'SARIMA':<8} {'VAR':<8}"
    
    print(border)
    print(header)
    print(border)
    
    for _, row in df.iterrows():
        print(f"{row['Country']:<10} {row['AR']:<8.3f} {row['ARIMA']:<8.3f} {row['SARIMA']:<8.3f} {row['VAR']:<8.3f}")
    
    print(border)

if __name__ == "__main__":
    create_comparison_table()