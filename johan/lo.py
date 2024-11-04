import requests
import pandas as pd
from datetime import datetime, timedelta

# Define API parameters
api_key = 'b4cdff3904bd493c94ff94160054a6e6'
base_url = 'https://api.weatherbit.io/v2.0/history/hourly'
location = {'lat': 58.1465, 'lon': 7.9956}  # Coordinates for Kristiansand

# Define date range
start_date = datetime(2015, 12, 31, 23)
end_date = datetime(2018, 9, 12, 23)

# Initialize a list to store temperature data
temperature_data = []

# Function to retrieve data in 10-day chunks
def fetch_data(start, end):
    params = {
        'lat': location['lat'],
        'lon': location['lon'],
        'start_date': start.strftime('%Y-%m-%d:%H'),
        'end_date': end.strftime('%Y-%m-%d:%H'),
        'key': api_key,
        'units': 'M',  # Metric units (Celsius)
        'tz': 'utc'
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    return data['data'] if 'data' in data else []

# Loop through date range in 10-day increments
date = start_date
while date < end_date:
    next_date = min(date + timedelta(days=10), end_date)
    data_chunk = fetch_data(date, next_date)
    temperature_data.extend(data_chunk)
    date = next_date + timedelta(hours=1)  # Move to the next chunk

# Convert to DataFrame
df = pd.DataFrame(temperature_data)

# Select only the relevant columns
df = df[['timestamp_utc', 'temp']]

# Rename columns for readability
df.columns = ['datetime_utc', 'temperature']

# Display the final DataFrame
print(df)
