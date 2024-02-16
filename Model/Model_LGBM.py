import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import lightgbm as lgb
from sklearn.metrics import mean_absolute_error

# Specify the path to your directory
directory_path = 'C:/Users/acer/OneDrive/Desktop/Ds Project/'

# Print the contents of the directory
for dirname, _, filenames in os.walk(directory_path):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Ignore warnings
warnings.filterwarnings("ignore")

# Loading data from CSV file
df = pd.read_csv('C:/Users/acer/OneDrive/Desktop/Ds Project/data.csv')

# Preview the first few rows of the DataFrame
print("Preview of the DataFrame:")
print(df.head())

# View summary of dataset
df.info()

# Creating a single column for date and time
df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
df = df.drop(['Date', 'Time'], axis=1)
df.set_index('Datetime', inplace=True)

# Resample the data to calculate the hourly sum
hourly_sum = df.resample('H').sum()
hourly_sum.reset_index(inplace=True)
hourly_sum.fillna(0, inplace=True)
print(hourly_sum.head())

# Resample the data to year, month, day, hour
hourly_sum['Year'] = hourly_sum['Datetime'].dt.year
hourly_sum['Month'] = hourly_sum['Datetime'].dt.month
hourly_sum['Day'] = hourly_sum['Datetime'].dt.day
hourly_sum['Hour'] = hourly_sum['Datetime'].dt.hour

# Print Values of the sensors
print(df['D11 (Belegungen/Intervall)'].value_counts())
print(df['D12 (Belegungen/Intervall)'].value_counts())
print(df['D21 (Belegungen/Intervall)'].value_counts())
print(df['D31 (Belegungen/Intervall)'].value_counts())
print(df['D41 (Belegungen/Intervall)'].value_counts())
print(df['D42 (Belegungen/Intervall)'].value_counts())
print(df['H53_M3_3006 (Belegungen/Intervall)'].value_counts())
print(df['H53_M6_1140 (Belegungen/Intervall)'].value_counts())
print(df['H57_M1_1137 (Belegungen/Intervall)'].value_counts())
print(df['A53_M5_3007 (Belegungen/Intervall)'].value_counts())

# Target variable selection
X = hourly_sum[['A53_M5_3007 (Belegungen/Intervall)', 'Year', 'Month', 'Day', 'Hour']]
y = hourly_sum['D11 (Belegungen/Intervall)']

# Split the dataset into the training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)

# Build the lightgbm model
regressor = lgb.LGBMRegressor()
regressor.fit(X_train, y_train)

# Predict the results
y_pred = regressor.predict(X_test)

# Evaluation Metric : MSE
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Evaluation Metric : MAE
mae = mean_absolute_error(y_test, y_pred)
print(f'Mean Absolute Error: {mae}')
y_test = np.where(y_test == 0, 1e-100, y_test)
mean_actual = sum(y_test) / len(y_test) 
mae_percentage = (mae / mean_actual) * 100
print(f"MAE as Percentage: {mae_percentage:.2f}%")

# Evaluation Metric : SMAPE
smape_score = 100/len(y_test) * np.sum(2 * np.abs(y_pred - y_test) / (np.abs(y_pred) + np.abs(y_test)))
print(f'Smape: {smape_score}')

# Compare model predictions with original results
comparison_df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
print(comparison_df.head())

# Plotting
plt.figure(figsize=(20, 6))
plt.plot(comparison_df.index, comparison_df['Actual'], label='Actual', marker='o')
plt.plot(comparison_df.index, comparison_df['Predicted'], label='Predicted', marker='x')
plt.title('Actual vs. Predicted Values')
plt.xlabel('Index')
plt.ylabel('Belegungen/Intervall')  
plt.legend()
plt.show()








