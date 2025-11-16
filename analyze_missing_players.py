import pandas as pd
import glob

print("Analyzing player coverage in player_info.csv...")

# Read the player_info.csv file
player_info = pd.read_csv('data/csv/players/player_info.csv')
existing_player_ids = set(player_info['id'].unique())
print(f"Players in player_info.csv: {len(existing_player_ids)}")

# Get all boxscore CSV files
boxscore_files = glob.glob('data/csv/boxscores/mlb_boxscores_*.csv')
print(f"Found {len(boxscore_files)} boxscore files")

# Collect all unique player IDs from boxscores
all_boxscore_player_ids = set()

for file in boxscore_files[:5]:  # Check first 5 files to start
    print(f"Processing {file}...")
    df = pd.read_csv(file)
    player_ids_in_file = set(df['player_id'].unique())
    all_boxscore_player_ids.update(player_ids_in_file)
    print(f"  Unique player IDs in this file: {len(player_ids_in_file)}")

print(f"\nTotal unique player IDs in checked boxscores: {len(all_boxscore_player_ids)}")

# Find missing player IDs
missing_player_ids = all_boxscore_player_ids - existing_player_ids
print(f"Missing player IDs in player_info.csv: {len(missing_player_ids)}")

if missing_player_ids:
    print("Sample missing player IDs:")
    for i, pid in enumerate(sorted(missing_player_ids)):
        if i < 10:  # Show first 10
            print(f"  {pid}")
        else:
            break
    
    # Save missing player IDs to file
    missing_df = pd.DataFrame({'missing_player_id': sorted(missing_player_ids)})
    missing_df.to_csv('data/csv/players/missing_player_ids.csv', index=False)
    print(f"Missing player IDs saved to data/csv/players/missing_player_ids.csv")