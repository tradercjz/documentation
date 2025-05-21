import pandas as pd
import numpy as np
from scipy.optimize import fmin
from datetime import datetime, timedelta

# Read the data
file_path =  '<YourDir>/curveOneday.csv'
data = pd.read_csv(file_path)

# Rename columns for convenience
data.rename(columns={'B_ANAL_CURVETERM': 'Maturity', 'B_ANAL_YIELD': 'Yield'}, inplace=True)

# Filter the data where B_ANAL_CURVETERM (Maturity) > 0
data = data[data['Maturity'] > 0]

# Define the Nelson-Siegel-Svensson formula
def nss_formula(df, beta0, beta1, beta2, beta3, tau1, tau2):
    term1 = beta0
    term2 = beta1 * (1 - np.exp(-df['Maturity'] / tau1)) / (df['Maturity'] / tau1)
    term3 = beta2 * ((1 - np.exp(-df['Maturity'] / tau1)) / (df['Maturity'] / tau1) - np.exp(-df['Maturity'] / tau1))
    term4 = beta3 * ((1 - np.exp(-df['Maturity'] / tau2)) / (df['Maturity'] / tau2) - np.exp(-df['Maturity'] / tau2))
    return term1 + term2 + term3 + term4

# Function to calculate residuals
def calc_residuals(params, df):
    beta0, beta1, beta2, beta3, tau1, tau2 = params
    df_copy = df.copy()  # Make a copy to avoid modifying the original DataFrame
    df_copy['NSS'] = nss_formula(df_copy, beta0, beta1, beta2, beta3, tau1, tau2)
    df_copy['Residual'] = (df_copy['Yield'] - df_copy['NSS']) ** 2
    return df_copy['Residual'].sum()


# Function to get NSS parameters for a specific date and curve number
def get_nss(data, dt, curverno):
    data1 = data.copy()
    group = data1[(data1['TRADE_DT'] == dt) & (data1['B_ANAL_CURVENUMBER'] == curverno)]
    initial_guess = [0.01, 0.01, 0.01, 0.01, 1.00, 1.00]
    params = fmin(calc_residuals, initial_guess, args=(group,), disp=False)
    return params

# Get distinct dates and curve numbers
distinct_dates = data['TRADE_DT'].unique()
distinct_curvenumbers = data['B_ANAL_CURVENUMBER'].unique()

# Create a dataframe with all combinations of distinct dates and curve numbers
params = pd.DataFrame([(dt, curverno) for dt in distinct_dates for curverno in distinct_curvenumbers], columns=['dt', 'curverno'])

# Timer to measure performance
import time
start_time = time.time()

results = []
for idx, row in params.iterrows():
    dt, curverno = row['dt'], row['curverno']
    params_values = get_nss(data, dt, curverno)
    result_dict = {
        'TRADE_DT': dt,
        'B_ANAL_CURVENUMBER': curverno,
        'beta0': params_values[0],
        'beta1': params_values[1],
        'beta2': params_values[2],
        'beta3': params_values[3],
        'tau1': params_values[4],
        'tau2': params_values[5]
    }
    results.append(result_dict)

result_df = pd.DataFrame(results)


end_time = time.time()

print(f"Time taken: {end_time - start_time} seconds")


# 扩展成1周数据的性能测试
# 生成日期
start_date = datetime(2022, 1, 1)
end_date = datetime(2022, 1, 7)
date_range = pd.date_range(start=start_date, end=end_date)
full_week_data = pd.concat([data]*len(date_range), ignore_index=True)
full_week_data['TRADE_DT'] = np.repeat(date_range, len(data))

# Get distinct dates and curve numbers
distinct_dates = full_week_data['TRADE_DT'].unique()
distinct_curvenumbers = full_week_data['B_ANAL_CURVENUMBER'].unique()

# Create a dataframe with all combinations of distinct dates and curve numbers
params = pd.DataFrame([(dt, curverno) for dt in distinct_dates for curverno in distinct_curvenumbers], columns=['dt', 'curverno'])
# Define the structure of the result dataframe
result_df = pd.DataFrame(columns=['TRADE_DT', 'B_ANAL_CURVENUMBER', 'beta0', 'beta1', 'beta2', 'beta3', 'tau1', 'tau2'])

# Timer to measure performance
import time
print("Before Week Calculate")
start_time = time.time()

results = []
for idx, row in params.iterrows():
    dt, curverno = row['dt'], row['curverno']
    params_values = get_nss(full_week_data, dt, curverno)
    result_dict = {
        'TRADE_DT': dt,
        'B_ANAL_CURVENUMBER': curverno,
        'beta0': params_values[0],
        'beta1': params_values[1],
        'beta2': params_values[2],
        'beta3': params_values[3],
        'tau1': params_values[4],
        'tau2': params_values[5]
    }
    results.append(result_dict)

result_df = pd.DataFrame(results)

end_time = time.time()

print(f"Week Time taken: {end_time - start_time} seconds")

# 扩展成1个月数据的性能测试
start_date = datetime(2022, 1, 1)
end_date = datetime(2022, 1, 31)
date_range = pd.date_range(start=start_date, end=end_date)
# 扩展数据到一个月
full_month_data = pd.concat([data]*len(date_range), ignore_index=True)
full_month_data['TRADE_DT'] = np.repeat(date_range, len(data))

# Get distinct dates and curve numbers
distinct_dates = full_month_data['TRADE_DT'].unique()
distinct_curvenumbers = full_month_data['B_ANAL_CURVENUMBER'].unique()

# Create a dataframe with all combinations of distinct dates and curve numbers
params = pd.DataFrame([(dt, curverno) for dt in distinct_dates for curverno in distinct_curvenumbers], columns=['dt', 'curverno'])
# Define the structure of the result dataframe
result_df = pd.DataFrame(columns=['TRADE_DT', 'B_ANAL_CURVENUMBER', 'beta0', 'beta1', 'beta2', 'beta3', 'tau1', 'tau2'])

# Timer to measure performance
import time
print("Before Week Calculate")
start_time = time.time()

results = []
for idx, row in params.iterrows():
    dt, curverno = row['dt'], row['curverno']
    params_values = get_nss(full_month_data, dt, curverno)
    result_dict = {
        'TRADE_DT': dt,
        'B_ANAL_CURVENUMBER': curverno,
        'beta0': params_values[0],
        'beta1': params_values[1],
        'beta2': params_values[2],
        'beta3': params_values[3],
        'tau1': params_values[4],
        'tau2': params_values[5]
    }
    results.append(result_dict)

result_df = pd.DataFrame(results)

end_time = time.time()

print(f"Month Time taken: {end_time - start_time} seconds")
