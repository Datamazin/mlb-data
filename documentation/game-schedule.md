# MLB Game Schedule Data Fields

## Overview
This document outlines the data fields available in the MLB game schedule dataset (`game_schedule.csv`). The current dataset contains 60+ fields with comprehensive game information from schedule through final results.

## Data Field Categories

### Core Game Identification Fields
| Field | Description | Type | Example |
|-------|-------------|------|---------|
| `gamePk` | Unique game identifier (primary key) | Integer | 778498 |
| `gameGuid` | Global unique identifier | String | 8ac61454-7fa7-4f37-94c0-47612575dbd8 |
| `season` | Season year | Integer | 2025 |
| `gameDate` | Scheduled game date/time (UTC) | DateTime | 2025-04-01T22:40:00Z |
| `officialDate` | Official game date (local) | Date | 2025-04-01 |
| `gameType` | Game type (R=Regular Season, P=Playoff, etc.) | String | R |
| `link` | API link to game feed | String | /api/v1.1/game/778498/feed/live |

### Game Status & State Fields
| Field | Description | Type | Example |
|-------|-------------|------|---------|
| `status.abstractGameState` | High-level status | String | Final |
| `status.codedGameState` | Coded status | String | F |
| `status.detailedState` | Detailed status description | String | Final |
| `status.statusCode` | Status code | String | F |
| `status.startTimeTBD` | Whether start time is TBD | Boolean | False |
| `status.abstractGameCode` | Abstract game code | String | F |
| `status.reason` | Status reason (if applicable) | String | - |

### Away Team Information
| Field | Description | Type | Example |
|-------|-------------|------|---------|
| `teams.away.team.id` | Away team ID | Integer | 140 |
| `teams.away.team.name` | Away team name | String | Texas Rangers |
| `teams.away.team.link` | Away team API link | String | /api/v1/teams/140 |
| `teams.away.score` | Away team final score | Float | 1.0 |
| `teams.away.isWinner` | Whether away team won | Boolean | True |
| `teams.away.splitSquad` | Split squad indicator | Boolean | False |
| `teams.away.seriesNumber` | Series number | Integer | 2 |
| `teams.away.leagueRecord.wins` | Away team wins | Integer | 4 |
| `teams.away.leagueRecord.losses` | Away team losses | Integer | 2 |
| `teams.away.leagueRecord.pct` | Away team win percentage | String | .667 |

### Home Team Information
| Field | Description | Type | Example |
|-------|-------------|------|---------|
| `teams.home.team.id` | Home team ID | Integer | 113 |
| `teams.home.team.name` | Home team name | String | Cincinnati Reds |
| `teams.home.team.link` | Home team API link | String | /api/v1/teams/113 |
| `teams.home.score` | Home team final score | Float | 0.0 |
| `teams.home.isWinner` | Whether home team won | Boolean | False |
| `teams.home.splitSquad` | Split squad indicator | Boolean | False |
| `teams.home.seriesNumber` | Series number | Integer | 2 |
| `teams.home.leagueRecord.wins` | Home team wins | Integer | 2 |
| `teams.home.leagueRecord.losses` | Home team losses | Integer | 3 |
| `teams.home.leagueRecord.pct` | Home team win percentage | String | .400 |

### Venue & Location Information
| Field | Description | Type | Example |
|-------|-------------|------|---------|
| `venue.id` | Venue ID | Integer | 2602 |
| `venue.name` | Venue name | String | Great American Ball Park |
| `venue.link` | Venue API link | String | /api/v1/venues/2602 |

### Game Details & Scheduling
| Field | Description | Type | Example |
|-------|-------------|------|---------|
| `dayNight` | Day or night game | String | night |
| `scheduledInnings` | Scheduled innings | Integer | 9 |
| `doubleHeader` | Double header indicator | String | N |
| `gameNumber` | Game number | Integer | 1 |
| `publicFacing` | Public facing indicator | Boolean | True |
| `gamedayType` | Gameday type | String | P |
| `tiebreaker` | Tiebreaker indicator | String | N |
| `reverseHomeAwayStatus` | Reverse home/away status | Boolean | False |
| `inningBreakLength` | Inning break length (minutes) | Integer | 120 |
| `isTie` | Whether game ended in tie | Boolean | False |

### Series Information
| Field | Description | Type | Example |
|-------|-------------|------|---------|
| `gamesInSeries` | Total games in series | Integer | 3 |
| `seriesGameNumber` | Game number within series | Integer | 2 |
| `seriesDescription` | Series type description | String | Regular Season |

### Administrative Fields
| Field | Description | Type | Example |
|-------|-------------|------|---------|
| `calendarEventID` | Calendar event identifier | String | 14-778498-2025-04-01 |
| `seasonDisplay` | Season display value | String | 2025 |
| `recordSource` | Record source | String | S |
| `ifNecessary` | If necessary indicator | String | N |
| `ifNecessaryDescription` | If necessary description | String | Normal Game |
| `content.link` | Link to game content | String | /api/v1/game/778498/content |

### Rescheduling & Special Circumstances
| Field | Description | Type | Example |
|-------|-------------|------|---------|
| `description` | Game description | String | Makeup of 5/6 PPD |
| `rescheduleDate` | Rescheduled date | DateTime | - |
| `rescheduleGameDate` | Rescheduled game date | Date | - |
| `rescheduledFrom` | Original scheduled date | DateTime | 2025-05-07T00:40:00Z |
| `rescheduledFromDate` | Original scheduled date | Date | 2025-05-06 |
| `resumeDate` | Resume date | DateTime | - |
| `resumeGameDate` | Resume game date | Date | - |
| `resumedFrom` | Resumed from date | DateTime | - |
| `resumedFromDate` | Resumed from date | Date | - |

## Recommended Simplified Extract Fields

For streamlined data analysis and reporting, the following **essential fields** are recommended:

### Minimal Game Schedule Extract
```csv
gamePk,season,gameDate,officialDate,gameType,status,
awayTeamId,awayTeamName,awayScore,awayWins,awayLosses,
homeTeamId,homeTeamName,homeScore,homeWins,homeLosses,
winner,venueId,venueName,dayNight,seriesGame,totalGames,
doubleHeader,rescheduled,description
```

### Field Mapping for Simplified Extract
| Simplified Field | Source Field | Purpose |
|------------------|--------------|---------|
| `gamePk` | `gamePk` | Unique identifier |
| `season` | `season` | Season year |
| `gameDate` | `gameDate` | Scheduled date/time |
| `officialDate` | `officialDate` | Official game date |
| `gameType` | `gameType` | Game type |
| `status` | `status.abstractGameState` | Game status |
| `awayTeamId` | `teams.away.team.id` | Away team ID |
| `awayTeamName` | `teams.away.team.name` | Away team name |
| `awayScore` | `teams.away.score` | Away team score |
| `awayWins` | `teams.away.leagueRecord.wins` | Away team wins |
| `awayLosses` | `teams.away.leagueRecord.losses` | Away team losses |
| `homeTeamId` | `teams.home.team.id` | Home team ID |
| `homeTeamName` | `teams.home.team.name` | Home team name |
| `homeScore` | `teams.home.score` | Home team score |
| `homeWins` | `teams.home.leagueRecord.wins` | Home team wins |
| `homeLosses` | `teams.home.leagueRecord.losses` | Home team losses |
| `winner` | Derived from `isWinner` fields | Winning team |
| `venueId` | `venue.id` | Venue ID |
| `venueName` | `venue.name` | Venue name |
| `dayNight` | `dayNight` | Day/night indicator |
| `seriesGame` | `seriesGameNumber` | Game number in series |
| `totalGames` | `gamesInSeries` | Total games in series |
| `doubleHeader` | `doubleHeader` | Double header indicator |
| `rescheduled` | Derived from `rescheduleDate` | Reschedule indicator |
| `description` | `description` | Special circumstances |

## Data Quality Notes

### Game Status Values
- **Final**: Game completed
- **Scheduled**: Game not yet started
- **In Progress**: Game currently being played
- **Postponed**: Game postponed
- **Cancelled**: Game cancelled

### Team Record Accuracy
- Team records (`wins`, `losses`, `pct`) reflect standings at time of game
- Useful for analysis of team performance trends
- Win percentages are stored as strings (e.g., ".667")

### Special Game Types
- **R**: Regular Season
- **P**: Playoff/Postseason
- **E**: Exhibition
- **S**: Spring Training

### Data Completeness
- All scheduled games have complete metadata
- Scores only populated for completed games
- Rescheduling fields only populated when applicable
- Venue information complete for all games

## Usage Examples

### Finding Games by Date
```sql
SELECT * FROM game_schedule 
WHERE officialDate = '2025-07-18'
```

### Finding Team Performance
```sql
SELECT awayTeamName, awayWins, awayLosses 
FROM game_schedule 
WHERE awayTeamName = 'New York Yankees'
```

### Finding Final Games
```sql
SELECT * FROM game_schedule 
WHERE status = 'Final'
```

---

**Last Updated**: November 16, 2025  
**Data Source**: MLB Stats API  
**File Location**: `data/game_schedule.csv`