import requests
import pandas as pd

# Set the date range for the schedule (example: July 5, 2025)
start_date = "2025-04-01"
end_date = "2025-07-05"

# MLB Schedule API endpoint
url = f"https://statsapi.mlb.com/api/v1/schedule?startDate={start_date}&endDate={end_date}&sportId=1"

response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    # Flatten the games list
    games = []
    for date in data.get("dates", []):
        for game in date.get("games", []):
            games.append(game)
    # Normalize and save to CSV
    df = pd.json_normalize(games)
    df.to_csv("game_schedule.csv", index=False)
    print(f"Saved {len(games)} games to game_schedule.csv")
else:
    print(f"Failed to fetch schedule: {response.status_code}")