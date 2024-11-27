#
# Time Differences Summary:
# count    151808.00
# mean        240.33
# std        5735.70
# min           0.00
# 25%           5.00
# 50%         149.00
# 75%         305.00
# max     1648436.00
#
# Oldest Data Entry Time: 2023-10-02 14:44:01+03:00
# Newest Data Entry Time: 2024-11-27 21:06:04+03:00
#
#
import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt

# Parse the XML file
file_path = "data/2/apple-health/export.xml"  # Replace with the actual file path
tree = ET.parse(file_path)
root = tree.getroot()

# List to store extracted data
heart_rate_data = []

# Iterate through records and extract data
for record in root.findall("Record"):
    if record.get("type") == "HKQuantityTypeIdentifierHeartRate":
        creation_date = record.get("creationDate")
        bpm = float(record.get("value"))  # Use float to handle decimal values
        heart_rate_data.append({"Creation Date": creation_date, "Heart Rate (BPM)": bpm})

# Convert to DataFrame
df = pd.DataFrame(heart_rate_data)

# Convert "Creation Date" to datetime
df['Creation Date'] = pd.to_datetime(df['Creation Date'])

# Sort by datetime
df = df.sort_values(by="Creation Date").reset_index(drop=True)

# Calculate time differences between consecutive records
df['Time Difference (s)'] = df['Creation Date'].diff().dt.total_seconds()

pd.options.display.float_format = '{:.2f}'.format

# Display the summary
print("Time Differences Summary:")
print(df['Time Difference (s)'].describe())

# Find the oldest data entry time
oldest_entry = df['Creation Date'].min()

# Find the newest data entry time
newest_entry = df['Creation Date'].max()

# Display the results
print(f"Oldest Data Entry Time: {oldest_entry}")
print(f"Newest Data Entry Time: {newest_entry}")

