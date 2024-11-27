import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt

# Parse the XML file
file_path = "data/2/apple-health/export.xml"  # Replace with the actual file path
tree = ET.parse(file_path)
root = tree.getroot()

# List to store extracted data
step_count_data = []

# Iterate through records and extract data
for record in root.findall("Record"):
    if record.get("type") == "HKQuantityTypeIdentifierStepCount":
        creation_date = record.get("creationDate")
        start_date = record.get("startDate")
        end_date = record.get("endDate")
        steps = int(float(record.get("value")))  # Convert value to integer
        step_count_data.append({
            "Creation Date": creation_date,
            "Start Date": start_date,
            "End Date": end_date,
            "Step Count": steps
        })

# Convert to DataFrame
df = pd.DataFrame(step_count_data)

# Convert "Creation Date" to datetime
df['Creation Date'] = pd.to_datetime(df['Creation Date'])
df['Start Date'] = pd.to_datetime(df['Start Date'])
df['End Date'] = pd.to_datetime(df['End Date'])

# Sort by creation date
df = df.sort_values(by="Creation Date").reset_index(drop=True)

# Filter the data for the specific date range
start_date = pd.to_datetime("2023-10-02 14:44:01+03:00")
end_date = pd.to_datetime("2024-11-27 21:06:04+03:00")
filtered_df = df[(df['Creation Date'] >= start_date) & (df['Creation Date'] <= end_date)]

# Additional filter: Remove step counts less than X = 100
filtered_df = filtered_df[filtered_df['Step Count'] >= 100]

# Display the first few rows of the filtered data
print(filtered_df.head())

# Visualize the filtered data points
plt.figure(figsize=(12, 6))
plt.plot(filtered_df['Creation Date'], filtered_df['Step Count'], marker='o', linestyle='-', color='blue', label='Step Count')
plt.title('Step Count Over Time (Filtered by Date and Step Count)')
plt.xlabel('Time')
plt.ylabel('Step Count')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.legend()
plt.tight_layout()
plt.show()

# Extract the timestamps for step counts < X
timestamps = filtered_df['Creation Date'].tolist()

# Save the timestamps to a CSV file
filtered_df[['Creation Date', 'Step Count']].to_csv('timestamps_less_than_100.csv', index=False)

print("CSV file 'timestamps_less_than_100.csv' has been created.")
