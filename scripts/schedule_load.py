import pandas as pd
import pyodbc

# Columns that should be decimal(5,3)
decimal_53_cols = ['teams_away_leagueRecord_pct', 'teams_home_leagueRecord_pct']
# Columns that should be decimal(4,1)
decimal_41_cols = ['teams_away_score', 'teams_home_score']

# Load the CSV
df = pd.read_csv('game_schedule.csv')

# Clean decimal(5,3) columns
for col in decimal_53_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').round(3)
        df.loc[(df[col].abs() > 99.999), col] = None

# Clean decimal(4,1) columns
for col in decimal_41_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').round(1)
        df.loc[(df[col].abs() > 999.9), col] = None

# Replace dots with underscores in column names
df.columns = [col.replace('.', '_') for col in df.columns]

# Replace NaN with None for SQL compatibility
df = df.where(pd.notnull(df), None)

# Ensure DataFrame columns match the insert statement order and count
columns = [
    'gamePk', 'gameGuid', 'link', 'gameType', 'season', 'gameDate', 'officialDate', 'isTie', 'gameNumber', 'publicFacing',
    'doubleHeader', 'gamedayType', 'tiebreaker', 'calendarEventID', 'seasonDisplay', 'dayNight', 'scheduledInnings',
    'reverseHomeAwayStatus', 'inningBreakLength', 'gamesInSeries', 'seriesGameNumber', 'seriesDescription',
    'recordSource', 'ifNecessary', 'ifNecessaryDescription', 'status_abstractGameState', 'status_codedGameState',
    'status_detailedState', 'status_statusCode', 'status_startTimeTBD', 'status_abstractGameCode',
    'teams_away_leagueRecord_wins', 'teams_away_leagueRecord_losses', 'teams_away_leagueRecord_pct',
    'teams_away_score', 'teams_away_team_id', 'teams_away_team_name', 'teams_away_team_link', 'teams_away_isWinner',
    'teams_away_splitSquad', 'teams_away_seriesNumber', 'teams_home_leagueRecord_wins', 'teams_home_leagueRecord_losses',
    'teams_home_leagueRecord_pct', 'teams_home_score', 'teams_home_team_id', 'teams_home_team_name', 'teams_home_team_link',
    'teams_home_isWinner', 'teams_home_splitSquad', 'teams_home_seriesNumber', 'venue_id', 'venue_name', 'venue_link',
    'content_link', 'description', 'rescheduleDate', 'rescheduleGameDate', 'status_reason', 'rescheduledFrom',
    'rescheduledFromDate', 'resumeDate', 'resumeGameDate', 'resumedFrom', 'resumedFromDate'
]

df = df[columns]

# Connect to SQL Server
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-TJG2020;"
    "DATABASE=mlb;"
    "Trusted_Connection=yes;"
)
cursor = conn.cursor()

# Prepare the insert statement (excluding game_key, which is IDENTITY)
insert_sql = """
INSERT INTO dbo.game (
    gamePk, gameGuid, link, gameType, season, gameDate, officialDate, isTie, gameNumber, publicFacing,
    doubleHeader, gamedayType, tiebreaker, calendarEventID, seasonDisplay, dayNight, scheduledInnings,
    reverseHomeAwayStatus, inningBreakLength, gamesInSeries, seriesGameNumber, seriesDescription,
    recordSource, ifNecessary, ifNecessaryDescription, status_abstractGameState, status_codedGameState,
    status_detailedState, status_statusCode, status_startTimeTBD, status_abstractGameCode,
    teams_away_leagueRecord_wins, teams_away_leagueRecord_losses, teams_away_leagueRecord_pct,
    teams_away_score, teams_away_team_id, teams_away_team_name, teams_away_team_link, teams_away_isWinner,
    teams_away_splitSquad, teams_away_seriesNumber, teams_home_leagueRecord_wins, teams_home_leagueRecord_losses,
    teams_home_leagueRecord_pct, teams_home_score, teams_home_team_id, teams_home_team_name, teams_home_team_link,
    teams_home_isWinner, teams_home_splitSquad, teams_home_seriesNumber, venue_id, venue_name, venue_link,
    content_link, description, rescheduleDate, rescheduleGameDate, status_reason, rescheduledFrom,
    rescheduledFromDate, resumeDate, resumeGameDate, resumedFrom, resumedFromDate
) VALUES (
    ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
)
"""

# Insert each row, print errors for debugging
for row in df.itertuples(index=False, name=None):
    try:
        cursor.execute(insert_sql, *row)
    except Exception as e:
        print("Error with row:", row)
        print(e)
        break

conn.commit()
cursor.close()
conn.close()
print("Game table populated")