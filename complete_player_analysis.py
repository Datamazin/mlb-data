import pandas as pd
import glob
import requests
import time
from datetime import datetime

print("Creating COMPLETE player info from ALL boxscore data...")

# Get all unique player IDs from ALL boxscore files
print("Step 1: Collecting ALL unique player IDs from boxscore files...")
boxscore_files = glob.glob('data/csv/boxscores/mlb_boxscores_*.csv')
print(f"Found {len(boxscore_files)} boxscore files")

all_player_ids = set()
for i, file in enumerate(boxscore_files):
    if i % 20 == 0:
        print(f"Processing file {i+1}/{len(boxscore_files)}: {file}")
    
    df = pd.read_csv(file)
    player_ids_in_file = set(df['player_id'].unique())
    all_player_ids.update(player_ids_in_file)

print(f"Total unique player IDs found in ALL boxscores: {len(all_player_ids)}")

# Load existing updated player info
try:
    existing_player_info = pd.read_csv('data/csv/players/player_info_updated.csv')
    existing_player_ids = set(existing_player_info['id'].unique())
    print(f"Existing players in updated file: {len(existing_player_ids)}")
except FileNotFoundError:
    existing_player_info = pd.DataFrame()
    existing_player_ids = set()
    print("No updated player file found")

# Find any remaining missing player IDs
still_missing = all_player_ids - existing_player_ids
print(f"Still missing player IDs: {len(still_missing)}")

if still_missing:
    print("Fetching remaining missing players...")
    
    def fetch_player_data(player_id):
        url = f"https://statsapi.mlb.com/api/v1/people/{player_id}"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("people") and len(data["people"]) > 0:
                    return data["people"][0]
        except Exception as e:
            print(f"Error fetching player {player_id}: {str(e)}")
        return None
    
    additional_player_data = []
    failed_fetches = []
    
    for i, player_id in enumerate(sorted(still_missing)):
        if i % 25 == 0:
            print(f"Progress: {i}/{len(still_missing)} additional players fetched")
        
        player_data = fetch_player_data(player_id)
        if player_data:
            additional_player_data.append(player_data)
        else:
            failed_fetches.append(player_id)
        
        time.sleep(0.1)  # Be nice to the API
    
    print(f"Successfully fetched {len(additional_player_data)} additional players")
    print(f"Failed to fetch {len(failed_fetches)} players")
    
    if additional_player_data:
        additional_df = pd.json_normalize(additional_player_data)
        final_df = pd.concat([existing_player_info, additional_df], ignore_index=True)
    else:
        final_df = existing_player_info
    
    final_df = final_df.drop_duplicates(subset=['id'], keep='first')
    
    # Save the complete player info
    output_file = 'data/csv/players/player_info_complete.csv'
    final_df.to_csv(output_file, index=False)
    
    print(f"Complete player info saved to: {output_file}")
    print(f"Total players: {len(final_df)}")
    
else:
    print("No additional missing players found!")
    # Still save as complete version
    existing_player_info.to_csv('data/csv/players/player_info_complete.csv', index=False)

# Create a summary report
coverage_report = {
    'total_unique_players_in_boxscores': len(all_player_ids),
    'players_in_complete_file': len(final_df) if 'final_df' in locals() else len(existing_player_info),
    'coverage_percentage': (len(final_df) if 'final_df' in locals() else len(existing_player_info)) / len(all_player_ids) * 100,
    'missing_players': len(still_missing) - len(additional_player_data) if 'additional_player_data' in locals() else len(still_missing)
}

print(f"\n=== COVERAGE REPORT ===")
for key, value in coverage_report.items():
    if 'percentage' in key:
        print(f"{key}: {value:.2f}%")
    else:
        print(f"{key}: {value}")

print("\n=== HOW player_info.csv WAS ORIGINALLY CREATED ===")
print("Based on the analysis, it appears the original player_info.csv was created by:")
print("1. Collecting player IDs from a subset of boxscore data (not all files)")
print("2. Using the MLB Stats API to fetch player details")
print("3. The populate_player_dimension.py script was a template but incomplete")
print("4. Only 527 players were originally included, missing 379+ players from boxscores")
print(f"5. The updated version now includes {coverage_report['players_in_complete_file']} players with {coverage_report['coverage_percentage']:.1f}% coverage")