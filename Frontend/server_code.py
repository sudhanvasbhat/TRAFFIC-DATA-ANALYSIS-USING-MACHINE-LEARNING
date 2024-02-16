import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
from datetime import datetime
import anvil.server
import requests
import time
import os


# Define a list of file names
file_names = ["data_A005", "data_A006", "data_A028", "data_A030", "data_A012", "data_A023", "data_A032", "data_A110"]
data_dict = {}

# Loop through the file names and read the corresponding CSV files
for file_name in file_names:
    file_path = f"../Dataset/{file_name}.csv"
    try:
        data_dict[file_name] = pd.read_csv(file_path)
        print(f"Loaded data from {file_path}")
    except FileNotFoundError:
        print(f"File not found at path: {file_path}")

# DataFrame using its respective file name
data_A005 = data_dict.get("data_A005")
data_A006 = data_dict.get("data_A006")
data_A028 = data_dict.get("data_A028")
data_A030 = data_dict.get("data_A030")
data_A012 = data_dict.get("data_A012")
data_A023 = data_dict.get("data_A023")
data_A032 = data_dict.get("data_A032")
data_A110 = data_dict.get("data_A110")


# Splitting to features and target variable

print("\nSplitting into features and target variable, and fitting model ...\n")

X_05, y_05 = data_A005[['Year', 'Month', 'Day', 'Hour']], data_A005['D42 (Belegungen/Intervall)']
X_06, y_06 = data_A006[['Year', 'Month', 'Day', 'Hour']], data_A006['D10 (Belegungen/Intervall)']
X_28, y_28 = data_A028[['Year', 'Month', 'Day', 'Hour']], data_A028['V23 (Belegungen/Intervall)']
# X_29, y_29 = data_A029[['Year', 'Month', 'Day', 'Hour']], data_A029['traffic']
X_30, y_30 = data_A030[['Year', 'Month', 'Day', 'Hour']], data_A030['VD13 (Belegungen/Intervall)']
# newsets
X_12, y_12 = data_A012[['Year', 'Month', 'Day', 'Hour']], data_A012['D29 (Belegungen/Intervall)']
X_23, y_23 = data_A023[['Year', 'Month', 'Day', 'Hour']], data_A023['D55 (Belegungen/Intervall)']
X_32, y_32 = data_A032[['Year', 'Month', 'Day', 'Hour']], data_A032['D91 (Belegungen/Intervall)']
X_110, y_110 = data_A110[['Year', 'Month', 'Day', 'Hour']], data_A110['D11 (Belegungen/Intervall)']


rf_model_05 = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model_05.fit(X_05, y_05)

rf_model_06 = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model_06.fit(X_06, y_06)

rf_model_28 = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model_28.fit(X_28, y_28)

rf_model_30 = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model_30.fit(X_30, y_30)

rf_model_12 = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model_12.fit(X_12, y_12)

rf_model_23 = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model_23.fit(X_23, y_23)

rf_model_32 = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model_32.fit(X_32, y_32)

rf_model_110 = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model_110.fit(X_110, y_110)


# Future prediction
print("\nPredicting future traffic...\n")

start = pd.Timestamp(year=2023, month=5, day=13, hour=0)
end = pd.Timestamp(year=2024, month=2, day=29, hour=23)
# Generate the date range
date_range = pd.date_range(start=start, end=end, freq='H')

# Create the new DataFrame
X_future = pd.DataFrame({
    'Year': date_range.year,
    'Month': date_range.month,
    'Day': date_range.day,
    'Hour': date_range.hour
})

# Make predictions
y_future_05 = rf_model_05.predict(X_future)
y_future_06 = rf_model_06.predict(X_future)
y_future_28 = rf_model_28.predict(X_future)
y_future_30 = rf_model_30.predict(X_future)
#newsets
y_future_12 = rf_model_12.predict(X_future)
y_future_23 = rf_model_23.predict(X_future)
y_future_32 = rf_model_32.predict(X_future)
y_future_110 = rf_model_110.predict(X_future)


# Binning existing data for final transfer to frontend
print("\nBinning traffic into low,medium and high categories.\n")

A05_old = data_A005.copy()
A05_old = A05_old[['Year', 'Month', 'Day', 'Hour','D42 (Belegungen/Intervall)']]
A05_old['traffic'] = pd.cut(A05_old['D42 (Belegungen/Intervall)'], bins=3, labels=[0, 1,2])
A05_old.drop(['D42 (Belegungen/Intervall)'], axis=1, inplace=True)
A06_old = data_A006.copy()
A06_old = A06_old[['Year', 'Month', 'Day', 'Hour','D10 (Belegungen/Intervall)']]
A06_old['traffic'] = pd.cut(A06_old['D10 (Belegungen/Intervall)'], bins=3, labels=[0, 1,2])
A06_old.drop(['D10 (Belegungen/Intervall)'], axis=1, inplace=True)
A28_old = data_A028.copy()
A28_old = A28_old[['Year', 'Month', 'Day', 'Hour','V23 (Belegungen/Intervall)']]
A28_old['traffic'] = pd.cut(A28_old['V23 (Belegungen/Intervall)'], bins=3, labels=[0, 1,2])
A28_old.drop(['V23 (Belegungen/Intervall)'], axis=1, inplace=True)
A30_old = data_A030.copy()
A30_old = A30_old[['Year', 'Month', 'Day', 'Hour','VD13 (Belegungen/Intervall)']]
A30_old['traffic'] = pd.cut(A30_old['VD13 (Belegungen/Intervall)'], bins=3, labels=[0, 1,2])
A30_old.drop(['VD13 (Belegungen/Intervall)'], axis=1, inplace=True)
#newsets
A12_old = data_A012.copy()
A12_old = A12_old[['Year', 'Month', 'Day', 'Hour','D29 (Belegungen/Intervall)']]
A12_old['traffic'] = pd.cut(A12_old['D29 (Belegungen/Intervall)'], bins=3, labels=[0, 1,2])
A12_old.drop(['D29 (Belegungen/Intervall)'], axis=1, inplace=True)
A23_old = data_A023.copy()
A23_old = A23_old[['Year', 'Month', 'Day', 'Hour','D55 (Belegungen/Intervall)']]
A23_old['traffic'] = pd.cut(A23_old['D55 (Belegungen/Intervall)'], bins=3, labels=[0, 1,2])
A23_old.drop(['D55 (Belegungen/Intervall)'], axis=1, inplace=True)
A32_old = data_A032.copy()
A32_old = A32_old[['Year', 'Month', 'Day', 'Hour','D91 (Belegungen/Intervall)']]
A32_old['traffic'] = pd.cut(A32_old['D91 (Belegungen/Intervall)'], bins=3, labels=[0, 1,2])
A32_old.drop(['D91 (Belegungen/Intervall)'], axis=1, inplace=True)
A110_old = data_A110.copy()
A110_old = A110_old[['Year', 'Month', 'Day', 'Hour','D11 (Belegungen/Intervall)']]
A110_old['traffic'] = pd.cut(A110_old['D11 (Belegungen/Intervall)'], bins=3, labels=[0, 1,2])
A110_old.drop(['D11 (Belegungen/Intervall)'], axis=1, inplace=True)


# Convert predicted data to bins to identify low,medium and high traffic
bin_labels_05 = pd.cut(y_future_05, bins=3, labels=[0, 1, 2])
bin_labels_06 = pd.cut(y_future_06, bins=3, labels=[0, 1, 2])
bin_labels_28 = pd.cut(y_future_28, bins=3, labels=[0, 1, 2])
bin_labels_30 = pd.cut(y_future_30, bins=3, labels=[0, 1, 2])
#newsets
bin_labels_12 = pd.cut(y_future_12, bins=3, labels=[0, 1, 2])
bin_labels_23 = pd.cut(y_future_23, bins=3, labels=[0, 1, 2])
bin_labels_32 = pd.cut(y_future_32, bins=3, labels=[0, 1, 2])
bin_labels_110 = pd.cut(y_future_110, bins=3, labels=[0, 1, 2])

X_future_05 = X_future.copy()
X_future_05['traffic'] = bin_labels_05
X_future_06 = X_future.copy()
X_future_06['traffic'] = bin_labels_06
X_future_28 = X_future.copy()
X_future_28['traffic'] = bin_labels_28
X_future_30 = X_future.copy()
X_future_30['traffic'] = bin_labels_30
#newsets
X_future_12 = X_future.copy()
X_future_12['traffic'] = bin_labels_12
X_future_23 = X_future.copy()
X_future_23['traffic'] = bin_labels_23
X_future_32 = X_future.copy()
X_future_32['traffic'] = bin_labels_32
X_future_110 = X_future.copy()
X_future_110['traffic'] = bin_labels_110

#A05_complete = A05_old.append(X_future_05, ignore_index=True)
#A06_complete = A06_old.append(X_future_06, ignore_index=True)
#A28_complete = A28_old.append(X_future_28, ignore_index=True)
#A30_complete = A30_old.append(X_future_30, ignore_index=True)

A05_complete = pd.concat([A05_old, X_future_05], ignore_index=True)
A06_complete = pd.concat([A06_old, X_future_06], ignore_index=True)
A28_complete = pd.concat([A28_old, X_future_28], ignore_index=True)
A30_complete = pd.concat([A30_old, X_future_30], ignore_index=True)
#newsets
A12_complete = pd.concat([A12_old, X_future_12], ignore_index=True)
A23_complete = pd.concat([A23_old, X_future_23], ignore_index=True)
A32_complete = pd.concat([A32_old, X_future_32], ignore_index=True)
A110_complete = pd.concat([A110_old, X_future_110], ignore_index=True)
print("\nModel training and prediction complete.\n")

#X_future_05.head()



# 
# Server connect starts from here
# 

## To run locally
print("Please wait while server connects ...")
i = 0
while i<5:
    try:
        i = i+1
        time.sleep(5)
        print("Try {0} ".format(i))
        anvil.server.connect("roadsandmaps_key",  url="ws://localhost:3030/_/uplink")
    except e:
        print (e)
print("\nSuccessfully connected! \n")


@anvil.server.callable
def run_prediction(date_time):
    # Formatting user-given data
    date_time=str(date_time)
    year = int(date_time[0:4])
    month = int(date_time[5:7])
    day = int(date_time[8:10])
    hour = int(date_time[11:13])
    
    # Filtering to get the traffic data for specified year, month, and hour
    traffic_A05 = A05_complete[(A05_complete['Year'] == year) & (A05_complete['Month'] == month) & (A05_complete['Day'] == day) & (A05_complete['Hour'] == hour)]['traffic'].values[0]
    traffic_A06 = A06_complete[(A06_complete['Year'] == year) & (A06_complete['Month'] == month) & (A06_complete['Day'] == day) & (A06_complete['Hour'] == hour)]['traffic'].values[0]
    traffic_A28 = A28_complete[(A28_complete['Year'] == year) & (A28_complete['Month'] == month) & (A28_complete['Day'] == day) & (A28_complete['Hour'] == hour)]['traffic'].values[0]
    traffic_A30 = A30_complete[(A30_complete['Year'] == year) & (A30_complete['Month'] == month) & (A30_complete['Day'] == day) & (A30_complete['Hour'] == hour)]['traffic'].values[0]
    #newsets
    traffic_A12 = A12_complete[(A12_complete['Year'] == year) & (A12_complete['Month'] == month) & (A12_complete['Day'] == day) & (A12_complete['Hour'] == hour)]['traffic'].values[0]
    traffic_A23 = A23_complete[(A23_complete['Year'] == year) & (A23_complete['Month'] == month) & (A23_complete['Day'] == day) & (A23_complete['Hour'] == hour)]['traffic'].values[0]
    traffic_A32 = A32_complete[(A32_complete['Year'] == year) & (A32_complete['Month'] == month) & (A32_complete['Day'] == day) & (A32_complete['Hour'] == hour)]['traffic'].values[0]
    traffic_A110 = A110_complete[(A110_complete['Year'] == year) & (A110_complete['Month'] == month) & (A110_complete['Day'] == day) & (A110_complete['Hour'] == hour)]['traffic'].values[0]

    colour_code = {
      0 : "green",
      1 : "yellow",
      2 : "red"
    }
    
    
#     return as a dict with key being the intersection and the values as colors
    junction_traffic = {
      "A005" : colour_code[traffic_A05],
      "A006" : colour_code[traffic_A06],
      "A028" : colour_code[traffic_A28],
      "A029" : "grey",
      "A030" : colour_code[traffic_A30],
      "A012" : colour_code[traffic_A12],
      "A023" : colour_code[traffic_A23],
      "A032" : colour_code[traffic_A32],
      "A110" : colour_code[traffic_A110]
    }
    print("Selected date : {0}, {1}, {2} at {3} : 00".format(year,month,day,hour))
    return junction_traffic

@anvil.server.callable
def get_route(start, end):
    MAPBOX_ACCESS_TOKEN = 'pk.eyJ1Ijoic3VkaGFudmFiaGF0IiwiYSI6ImNscXhvZTY5OTBnODMyanBjdGlrZHZhNXcifQ.8ahjraPbjvx1dbiT6pdPgA'
    url = f"https://api.mapbox.com/directions/v5/mapbox/driving/{start[1]},{start[0]};{end[1]},{end[0]}?geometries=geojson&access_token={MAPBOX_ACCESS_TOKEN}"
    
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Error fetching route data")
    
anvil.server.wait_forever()