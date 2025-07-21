import requests
import pandas as pd
import json

# Read the CSV file with gamePk values
games_df = pd.read_csv('mlb_games_2025-07-05.csv')

boxscores = []
for game_pk in games_df['gamePk']:
    url = f'https://statsapi.mlb.com/api/v1/game/{game_pk}/boxscore'
    response = requests.get(url)
    if response.status_code == 200:
        boxscore_data = response.json()
        # You can customize what to extract; here we just store the full boxscore
        boxscores.append({'gamePk': game_pk, 'boxscore': boxscore_data})
    else:
        boxscores.append({'gamePk': game_pk, 'boxscore': None})

# Optionally, save all boxscores to a JSON file
with open('mlb_boxscores_2025-07-05.json', 'w') as f:
    json.dump(boxscores, f)