import pandas as pd
import requests
import time
from datetime import datetime
import json

print("Creating comprehensive player info from all boxscore data...")

# Load existing player info
try:
    existing_player_info = pd.read_csv('data/csv/players/player_info.csv')
    existing_player_ids = set(existing_player_info['id'].unique())
    print(f"Existing players in player_info.csv: {len(existing_player_ids)}")
except FileNotFoundError:
    existing_player_info = pd.DataFrame()
    existing_player_ids = set()
    print("No existing player_info.csv found, creating from scratch")

# Load missing player IDs
missing_players = pd.read_csv('data/csv/players/missing_player_ids.csv')
missing_player_ids = missing_players['missing_player_id'].tolist()
print(f"Missing player IDs to fetch: {len(missing_player_ids)}")

# Function to fetch player data from MLB API
def fetch_player_data(player_id):
    url = f"https://statsapi.mlb.com/api/v1/people/{player_id}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("people") and len(data["people"]) > 0:
                return data["people"][0]
        else:
            print(f"Failed to fetch player {player_id}: HTTP {response.status_code}")
    except Exception as e:
        print(f"Error fetching player {player_id}: {str(e)}")
    return None

# Fetch missing player data
new_player_data = []
failed_fetches = []

print("Fetching missing player data from MLB API...")
for i, player_id in enumerate(missing_player_ids):
    if i % 50 == 0:
        print(f"Progress: {i}/{len(missing_player_ids)} players fetched")
    
    player_data = fetch_player_data(player_id)
    if player_data:
        new_player_data.append(player_data)
    else:
        failed_fetches.append(player_id)
    
    # Be nice to the API
    time.sleep(0.1)

print(f"Successfully fetched: {len(new_player_data)} players")
print(f"Failed to fetch: {len(failed_fetches)} players")

if failed_fetches:
    print("Failed player IDs:", failed_fetches[:10])  # Show first 10 failures

# Convert to DataFrame
if new_player_data:
    new_players_df = pd.json_normalize(new_player_data)
    print(f"New players DataFrame shape: {new_players_df.shape}")
    print(f"New players columns: {list(new_players_df.columns)}")
    
    # Combine with existing data
    if not existing_player_info.empty:
        combined_df = pd.concat([existing_player_info, new_players_df], ignore_index=True)
    else:
        combined_df = new_players_df
    
    # Remove any duplicates based on player ID
    combined_df = combined_df.drop_duplicates(subset=['id'], keep='first')
    
    # Save the updated player info
    output_file = 'data/csv/players/player_info_updated.csv'
    combined_df.to_csv(output_file, index=False)
    
    print(f"Updated player info saved to: {output_file}")
    print(f"Total players: {len(combined_df)}")
    print(f"Total columns: {len(combined_df.columns)}")
    
    # Also backup the original if it exists
    if not existing_player_info.empty:
        backup_file = f'data/csv/players/player_info_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        existing_player_info.to_csv(backup_file, index=False)
        print(f"Original file backed up to: {backup_file}")

# Save failed player IDs for later retry
if failed_fetches:
    failed_df = pd.DataFrame({'failed_player_id': failed_fetches})
    failed_df.to_csv('data/csv/players/failed_player_fetches.csv', index=False)
    print(f"Failed player IDs saved to: data/csv/players/failed_player_fetches.csv")

print("Player info update complete!")