import json

# Load a sample JSON file to see the complete structure
with open('data/json/boxscores/mlb_boxscores_2025-04-03.json', 'r') as f:
    data = json.load(f)

# Check the first game's structure
game = data[0]
boxscore = game['boxscore']

print('=== BOXSCORE DATA STRUCTURE ===')
print(f'Game ID: {game["gamePk"]}')

# Check both teams
for team_type in ['away', 'home']:
    team = boxscore['teams'][team_type]
    print(f'\n{team_type.upper()} TEAM: {team["team"]["name"]}')
    
    # Check what player arrays exist
    print(f'  Batters: {len(team.get("batters", []))} players')
    print(f'  Pitchers: {len(team.get("pitchers", []))} players')
    print(f'  Bench: {len(team.get("bench", []))} players')
    print(f'  Bullpen: {len(team.get("bullpen", []))} players')
    
    # Show sample batter data structure
    if team.get('batters'):
        batter_id = team['batters'][0]
        player_key = f'ID{batter_id}'
        player = team['players'].get(player_key, {})
        
        print(f'\n  Sample batter ({batter_id}):')
        print(f'    Name: {player.get("person", {}).get("fullName", "N/A")}')
        print(f'    Batting Order: {player.get("battingOrder", "N/A")}')
        print(f'    Has batting stats: {"batting" in player.get("stats", {})}')
        print(f'    Has pitching stats: {"pitching" in player.get("stats", {})}')
        
        # Show actual batting stats
        batting_stats = player.get('stats', {}).get('batting', {})
        if batting_stats:
            print(f'    Sample batting stats: AB={batting_stats.get("atBats")}, H={batting_stats.get("hits")}, R={batting_stats.get("runs")}')
    
    # Show sample pitcher data structure  
    if team.get('pitchers'):
        pitcher_id = team['pitchers'][0]
        player_key = f'ID{pitcher_id}'
        player = team['players'].get(player_key, {})
        
        print(f'\n  Sample pitcher ({pitcher_id}):')
        print(f'    Name: {player.get("person", {}).get("fullName", "N/A")}')
        print(f'    Batting Order: {player.get("battingOrder", "N/A")}')
        print(f'    Has batting stats: {"batting" in player.get("stats", {})}')
        print(f'    Has pitching stats: {"pitching" in player.get("stats", {})}')
        
        # Show actual pitching stats if they exist
        pitching_stats = player.get('stats', {}).get('pitching', {})
        if pitching_stats:
            print(f'    Sample pitching stats: IP={pitching_stats.get("inningsPitched")}, H={pitching_stats.get("hits")}, ER={pitching_stats.get("earnedRuns")}')
        
        # Check if pitcher also has batting stats
        batting_stats = player.get('stats', {}).get('batting', {})
        if batting_stats:
            print(f'    Pitcher batting stats: AB={batting_stats.get("atBats")}, H={batting_stats.get("hits")}')

print('\n=== PROCESSING CONFIRMATION ===')
print('The CSV processing script (z02_all_boxscores.ipynb):')
print('1. Only processes players in the "batters" array')
print('2. Extracts only batting statistics from player.stats.batting')
print('3. Does NOT process pitchers array or pitching statistics')
print('4. Pitchers appear in CSV only if they also batted (rare in AL with DH)')