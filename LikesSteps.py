#
# Oldest Date: 2022-01-07 18:09:48
# Newest Date: 2024-11-23 10:36:28
#


import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load the JSON data
file_path = "data/your_instagram_activity/likes/liked_posts.json"  # Replace with your file path
with open(file_path, 'r') as file:
    data = json.load(file)

# Extract relevant data
likes_data = []
for item in data['likes_media_likes']:
    for like in item['string_list_data']:
        timestamp = like['timestamp']
        title = item.get('title', 'Unknown')
        likes_data.append({
            'Title': title,
            'Timestamp': timestamp
        })

# Convert to DataFrame
df = pd.DataFrame(likes_data)

# Convert timestamps to datetime
df['Date'] = pd.to_datetime(df['Timestamp'], unit='s')

# Extract additional temporal features
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month_name()
df['Day'] = df['Date'].dt.day_name()
df['Hour'] = df['Date'].dt.hour

# Aggregate Instagram likes by date
likes_per_day = df.groupby('Day').size().reset_index(name='Likes')

# Display the aggregated likes data
print(likes_per_day.head())

#################################

# Load step count data
step_data = pd.read_csv("filtered_step_data.csv")  # Replace with actual file path
step_data['Date'] = pd.to_datetime(step_data['Date'])  # Ensure Date is in datetime format

# Merge the datasets on the Date column
merged_data = pd.merge(step_data, likes_per_day, on='Day', how='outer')

# Fill missing values with 0 for visualization purposes
merged_data['Step Count'] = merged_data['Step Count'].fillna(0).astype(int)
merged_data['Likes'] = merged_data['Likes'].fillna(0).astype(int)

# Display the merged data
print(merged_data.head())



