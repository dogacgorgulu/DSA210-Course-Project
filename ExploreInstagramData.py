#
# Oldest Date: 2013-12-11 20:11:19
# Newest Date: 2024-11-27 18:11:33
#
#
#
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load the JSON data
file_path = "data/2/your_instagram_activity/likes/liked_posts.json" 
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

######

# Find oldest and newest dates
oldest_date = df['Date'].min()
newest_date = df['Date'].max()

print(f"Oldest Date: {oldest_date}")
print(f"Newest Date: {newest_date}")

##############################
#
# Like Counts by Year-Month
#
##############################

# Group by Year-Month
df['Year-Month'] = df['Date'].dt.to_period('M')  # Create Year-Month column

# Aggregate like counts by Year-Month
likes_by_month = df.groupby('Year-Month').size().reset_index(name='Like Count')

# Convert Year-Month to string for plotting
likes_by_month['Year-Month'] = likes_by_month['Year-Month'].astype(str)

# Extract year for background shading
likes_by_month['Year'] = likes_by_month['Year-Month'].str[:4]

# Plot the data
plt.figure(figsize=(12, 6))
plt.plot(likes_by_month['Year-Month'], likes_by_month['Like Count'], marker='o', label='Likes')

# Shade the background by year
unique_years = likes_by_month['Year'].unique()
current_color = 'lightblue'

for year in unique_years:
    # Find the range of months for the year
    year_months = likes_by_month[likes_by_month['Year'] == year]
    start_idx = likes_by_month.index[likes_by_month['Year-Month'] == year_months['Year-Month'].iloc[0]].tolist()[0]
    end_idx = likes_by_month.index[likes_by_month['Year-Month'] == year_months['Year-Month'].iloc[-1]].tolist()[0]

    # Add background shading
    plt.axvspan(start_idx - 0.5, end_idx + 0.5, color=current_color, alpha=0.2, label=year if current_color == 'lightblue' else None)

    # Alternate colors for each year
    current_color = 'lightgray' if current_color == 'lightblue' else 'lightblue'

# Customize the chart
plt.title('Likes Count by Month')
plt.xlabel('Month-Year')
plt.ylabel('Number of Likes')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y')
plt.tight_layout()
plt.legend()
plt.show()


