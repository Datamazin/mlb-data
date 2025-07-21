import requests
import pandas as pd

# Example: Get all player IDs (you would get these from your boxscore data)
# player_ids = [445276, 453286, ...]  # Fill with your IDs

player_data = []
for pid in player_ids:
    url = f"https://statsapi.mlb.com/api/v1/people/{pid}"
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
        if data.get("people"):
            player_data.append(data["people"][0])

# Flatten and save as CSV for dimension table
df = pd.json_normalize(player_data)
df.to_csv("player_dimension.csv", index=False)