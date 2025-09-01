import pandas as pd
from statsmodels.tsa.stattools import adfuller, kpss

CONFIG = {
    'date_format': '%Y-%m-%d',
    'p_value_threshold': 0.05,
    'enable_kpss_test': True,
    'enable_rolling_test': True,
    'rolling_window_size': 3,
    'adf_max_lag': None,  # None lets the function automatically determine the max lag
    'kpss_regression': 'c'  # Options: 'c' (constant), 'ct' (constant + trend)
}


def validate_inputs(time_series_data: pd.DataFrame):
    # Ensure required columns exist
    if 'Date' not in time_series_data.columns:
        raise ValueError("Time series data must have a 'Date' column.")

    # Check date formats and ensure consistency
    time_series_data['Date'] = pd.to_datetime(time_series_data['Date'], format=CONFIG['date_format'])

    # Check for missing values
    if time_series_data.isnull().values.any():
        raise ValueError("Time series data contains missing values.")

    return time_series_data

def test_stationarity(values):
    result = adfuller(values, maxlag=CONFIG['adf_max_lag'])
    return {
        'Test Statistic': result[0],
        'p-value': result[1],
        'Lags Used': result[2],
        'Number of Observations': result[3],
        'Critical Values': result[4],
        'Stationary': result[1] < CONFIG['p_value_threshold']
    }

def test_kpss(values):
    result = kpss(values, regression=CONFIG['kpss_regression'])
    return {
        'Test Statistic': result[0],
        'p-value': result[1],
        'Lags Used': result[2],
        'Critical Values': result[3],
        'Stationary': result[1] > CONFIG['p_value_threshold']
    }

def test_multiple_series(data: pd.DataFrame):
    results = {}
    for column in data.columns[1:]:  # Skip the 'Date' column
        values = data[column]
        series_results = {
            'ADF': test_stationarity(values)
        }
        if CONFIG['enable_kpss_test']:
            series_results['KPSS'] = test_kpss(values)
        results[column] = series_results
    return results
  
def main(df):

    try:
        validated_data = validate_inputs(df)

        print("\nStationarity Test Results for Multiple Series:")
        multi_series_results = test_multiple_series(validated_data)
        for series_name, results in multi_series_results.items():
            print(f"\nResults for {series_name}:")
            for test_name, test_results in results.items():
                print(f"  {test_name}:")
                for key, value in test_results.items():
                    print(f"    {key}: {value}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
