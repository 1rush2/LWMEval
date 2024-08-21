import xarray as xr
import numpy as np
import pygrib
import pandas as pd
from datetime import datetime

# Define the dates of interest
DATES = ["20230301", "20230601", "20230901", "20231201"]

# Open the Zarr dataset
ds = xr.open_zarr('gs://weatherbench2/datasets/era5-hourly-climatology/1990-2019_6h_1440x721.zarr')

# Extract relevant data
variables = {
    '2 metre temperature': ds['2m_temperature'],
    '10 metre U wind component': ds['10m_u_component_of_wind'],
    '10 metre V wind component': ds['10m_v_component_of_wind'],
    'Mean sea level pressure': ds['mean_sea_level_pressure'],
    'geopotential': ds['geopotential'].sel(level=500)
}

# Function to convert a date string to dayofyear
def date_to_dayofyear(date_str):
    date_obj = datetime.strptime(date_str, '%Y%m%d')
    return date_obj.timetuple().tm_yday

# # Function to read data from a GRIB file
# def read_data(file_path, name, index=0):
#     grib = pygrib.open(file_path)
#     data = grib.select(name=name)[index]
#     lats, lons = data.latlons()
#     values = data.values
#     values = np.nan_to_num(values, nan=219)  # Replace NaN with 219 or a relevant value
#     grib.close()
#     return np.column_stack((lats.flatten(), lons.flatten(), values.flatten()))
# # Extract relevant data

# Function to read data from a GRIB file
def read_data(file_path, name, index):
    level=500
    short_name='z'
    try:
        with pygrib.open(file_path) as grib:
            # Select the data by level and short name
            if var_name == 'geopotential':
                data = grib.select(level=level, shortName=short_name)[index]
            else:
                data = grib.select(name=name)[index]
            lats, lons = data.latlons()
            values = data.values
            values = np.nan_to_num(values, nan=219)  # Replace NaN with 219 or a relevant value
            return np.column_stack((lats.flatten(), lons.flatten(), values.flatten()))
    except (IOError, ValueError) as e:
        print(f"Error reading GRIB file {file_path}: {e}")
        return None

# Function to calculate latitude weights
def calculate_latitude_weights(lat_grid_resolution=0.25):
    total_lat_range = 180
    num_lat_cells = int(total_lat_range / lat_grid_resolution)
    theta_u = np.zeros(num_lat_cells)
    theta_l = np.zeros(num_lat_cells)
    for i in range(num_lat_cells):
        theta_l[i] = -90 + i * lat_grid_resolution
        theta_u[i] = theta_l[i] + lat_grid_resolution
    sin_theta_u = np.sin(np.radians(theta_u))
    sin_theta_l = np.sin(np.radians(theta_l))
    weights = (sin_theta_u - sin_theta_l) / np.mean(sin_theta_u - sin_theta_l)
    return weights

# Metric functions
def mse(true, pred):
    return np.mean((true[:, 2] - pred[:, 2])**2)

def rmse(true, pred):
    latitude_weights = calculate_latitude_weights()
    index_to_copy = 360
    new_index = index_to_copy + 1
    new_latitude_weights = np.insert(latitude_weights, new_index, latitude_weights[index_to_copy])
    weight = new_latitude_weights.repeat(1440)
    return np.sqrt((weight * np.square((true[:, 2] - pred[:, 2]))).mean())

def nrmse(true, pred):
    range_true = true[:, 2].max() - true[:, 2].min()
    if range_true == 0:
        return float('inf')
    return rmse(true, pred) / range_true

def bias(true, pred):
    latitude_weights = calculate_latitude_weights()
    index_to_copy = 360
    new_index = index_to_copy + 1
    new_latitude_weights = np.insert(latitude_weights, new_index, latitude_weights[index_to_copy])
    weight = new_latitude_weights.repeat(1440)
    return (np.abs(true[:, 2] - pred[:, 2])).mean()

def acc(true, pred, climatology):
    anomalies_true = true[:, 2] - climatology[:, 2]
    anomalies_pred = pred[:, 2] - climatology[:, 2]
    latitude_weights = calculate_latitude_weights()
    index_to_copy = 360
    new_index = index_to_copy + 1
    new_latitude_weights = np.insert(latitude_weights, new_index, latitude_weights[index_to_copy])
    weight = new_latitude_weights.repeat(1440)
    weighted_anomalies_true = anomalies_true * weight
    weighted_anomalies_pred = anomalies_pred * weight
    numerator = np.sum(weight * weighted_anomalies_true * weighted_anomalies_pred)
    denominator = np.sqrt(np.sum(weight * weighted_anomalies_true**2) * np.sum(weight * weighted_anomalies_pred**2))
    return numerator / denominator

def skill_score(true, pred, climatology):
    mse_f = mse(true, pred)
    mse_c = mse(true, climatology)
    return 1 - (mse_f / mse_c)

# Models and their corresponding index
models = {
    'fengwu.grib': 0,
    'fengwuv2.grib': 0,
    'fourcastnet.grib': 1,
    'fourcastnetv2-small.grib': 1,
    'fuxi.grib': 0,
    'graphcast.grib': 1,
    'panguweather.grib': 1
}

# Loop over the dates and calculate metrics
results_per_date = {}
for date in DATES:
    dayofyear = date_to_dayofyear(date)
    results_per_var = {}
    
    for var_name, var_data in variables.items():
        var_day = var_data.sel(dayofyear=dayofyear)
        var_day_6h = var_day.sel(hour=6)
        
        lats = var_day_6h['latitude'].values
        lons = var_day_6h['longitude'].values
        values = var_day_6h.values
        
        lon_grid, lat_grid = np.meshgrid(lons, lats)
        climatology_data = np.column_stack((lat_grid.flatten(), lon_grid.flatten(), values.flatten()))
        
        truth_file = f'/home/data2/ccrush/big_model/{date}-truth/panguweather.grib'
        truth_data = read_data(truth_file, var_name, 0)
        
        results = {}
        for model, index in models.items():
            pred_file = f'/home/data2/ccrush/big_model/{date}/{model}'
            pred_data = read_data(pred_file, var_name, index)
            results[model] = {
                'RMSE': rmse(truth_data, pred_data),
                'NRMSE': nrmse(truth_data, pred_data),
                'Bias': bias(truth_data, pred_data),
                'ACC': acc(truth_data, pred_data, climatology_data),
                'SS': skill_score(truth_data, pred_data, climatology_data)
            }
        
        results_per_var[var_name] = results
    
    results_per_date[date] = results_per_var

# Convert the results to a DataFrame
rows = []
for date, date_results in results_per_date.items():
    for var_name, var_results in date_results.items():
        for model, metrics in var_results.items():
            row = {'Date': date, 'Variable': var_name, 'Model': model}
            row.update(metrics)
            rows.append(row)

df = pd.DataFrame(rows)

# Save the DataFrame to an Excel file
output_file = 'model_performance_metrics_all_variables.xlsx'
df.to_excel(output_file, index=False)

print(f"Results have been saved to {output_file}")
