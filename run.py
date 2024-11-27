import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load the JSON data
file_path = "path_to_your_json_file.json"  # Replace with your file path
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

# Analyze temporal patterns
# 1. Likes by hour of the day
likes_by_hour = df.groupby('Hour').size()

# 2. Likes by day of the week
likes_by_day = df.groupby('Day').size()

# 3. Likes by month
likes_by_month = df.groupby('Month').size()

# Visualize the results
# Likes by Hour
plt.figure(figsize=(10, 6))
likes_by_hour.plot(kind='bar')
plt.title('Likes by Hour of Day')
plt.xlabel('Hour of Day')
plt.ylabel('Number of Likes')
plt.xticks(rotation=0)
plt.grid(axis='y')
plt.show()

# Likes by Day of Week
plt.figure(figsize=(10, 6))
likes_by_day.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).plot(kind='bar')
plt.title('Likes by Day of Week')
plt.xlabel('Day of Week')
plt.ylabel('Number of Likes')
plt.xticks(rotation=0)
plt.grid(axis='y')
plt.show()

# Likes by Month
plt.figure(figsize=(10, 6))
likes_by_month.reindex(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']).plot(kind='bar')
plt.title('Likes by Month')
plt.xlabel('Month')
plt.ylabel('Number of Likes')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.show()