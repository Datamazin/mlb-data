import json
import os

def analyze_batting_stats():
    """Analyze the batting statistics structure from a sample JSON file"""
    
    # Find a JSON file to analyze
    json_dir = 'data/json/boxscores'
    json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
    
    if not json_files:
        print("No JSON files found")
        return
    
    sample_file = os.path.join(json_dir, json_files[0])
    print(f"Analyzing: {sample_file}")
    
    with open(sample_file, 'r') as f:
        all_boxscores = json.load(f)
    
    batting_fields = set()
    sample_stats = None
    
    # Search through all games for batting statistics
    for game in all_boxscores:
        if game.get('boxscore'):
            teams = game['boxscore'].get('teams', {})
            for team_type in ['home', 'away']:
                team = teams.get(team_type, {})
                players = team.get('players', {})
                
                for player_key, player_data in players.items():
                    stats = player_data.get('stats', {})
                    batting = stats.get('batting', {})
                    
                    if batting:
                        batting_fields.update(batting.keys())
                        if sample_stats is None:
                            sample_stats = batting
                            print(f"\nSample batting stats from player {player_key}:")
                            for key, value in batting.items():
                                print(f"  {key}: {value} ({type(value).__name__})")
    
    print(f"\nAll available batting fields ({len(batting_fields)}):")
    for field in sorted(batting_fields):
        print(f"  - {field}")
    
    return sorted(batting_fields)

if __name__ == "__main__":
    fields = analyze_batting_stats()