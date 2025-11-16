# MLB Boxscore Data Structure

This document outlines the comprehensive data structure available in MLB boxscore JSON files, providing detailed information about each game's complete statistical breakdown.

## Overview

The boxscore data structure provides the most detailed view of MLB game statistics, including:
- Complete player statistics for both teams
- Detailed pitching and batting performance
- Game officials and venue information
- Team-level aggregated statistics
- Top performers and game highlights

## Data Source
- **API Endpoint**: MLB Stats API `/api/v1.1/game/{gamePk}/feed/live`
- **File Format**: JSON
- **Update Frequency**: Real-time during games, final after completion
- **Coverage**: All MLB regular season, playoff, and exhibition games

---

## Top-Level Structure

```json
[
  {
    "gamePk": 778470,
    "boxscore": {
      // Complete boxscore data structure
    }
  }
]
```

### Root Fields
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `gamePk` | Integer | Unique game identifier | 778470 |
| `boxscore` | Object | Complete boxscore data | See detailed structure below |

---

## Boxscore Object Structure

### Copyright and Metadata
| Field | Type | Description |
|-------|------|-------------|
| `copyright` | String | MLB copyright notice |

### Teams Structure
The `teams` object contains complete data for both away and home teams:

```json
{
  "teams": {
    "away": { /* Team data structure */ },
    "home": { /* Team data structure */ }
  }
}
```

## Team Data Structure

Each team (away/home) contains the following sections:

### Team Information
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `team.id` | Integer | Unique team ID | 111 |
| `team.name` | String | Full team name | "Boston Red Sox" |
| `team.abbreviation` | String | Team abbreviation | "BOS" |
| `team.teamCode` | String | Team code | "bos" |
| `team.teamName` | String | Team nickname | "Red Sox" |
| `team.locationName` | String | Team city | "Boston" |
| `team.firstYearOfPlay` | String | Franchise start year | "1901" |
| `team.franchiseName` | String | Franchise name | "Boston" |
| `team.clubName` | String | Club name | "Red Sox" |
| `team.shortName` | String | Short team name | "Boston" |
| `team.active` | Boolean | Team active status | true |

### League and Division Information
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `team.league.id` | Integer | League ID | 103 |
| `team.league.name` | String | League name | "American League" |
| `team.division.id` | Integer | Division ID | 201 |
| `team.division.name` | String | Division name | "American League East" |
| `team.sport.id` | Integer | Sport ID | 1 |
| `team.sport.name` | String | Sport name | "Major League Baseball" |

### Venue Information
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `team.venue.id` | Integer | Home venue ID | 3 |
| `team.venue.name` | String | Home venue name | "Fenway Park" |
| `team.springVenue.id` | Integer | Spring training venue ID | 4309 |

### Team Record
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `team.record.wins` | Integer | Season wins | 6 |
| `team.record.losses` | Integer | Season losses | 8 |
| `team.record.pct` | String | Winning percentage | ".429" |
| `team.record.winningPercentage` | String | Winning percentage | ".429" |

## Team Statistics

### Batting Statistics
Complete team batting statistics for the game:

| Field | Type | Description |
|-------|------|-------------|
| `teamStats.batting.atBats` | Integer | Total at-bats |
| `teamStats.batting.runs` | Integer | Runs scored |
| `teamStats.batting.hits` | Integer | Total hits |
| `teamStats.batting.doubles` | Integer | Doubles |
| `teamStats.batting.triples` | Integer | Triples |
| `teamStats.batting.homeRuns` | Integer | Home runs |
| `teamStats.batting.rbi` | Integer | Runs batted in |
| `teamStats.batting.baseOnBalls` | Integer | Walks |
| `teamStats.batting.strikeOuts` | Integer | Strikeouts |
| `teamStats.batting.leftOnBase` | Integer | Runners left on base |
| `teamStats.batting.avg` | String | Team batting average |
| `teamStats.batting.obp` | String | On-base percentage |
| `teamStats.batting.slg` | String | Slugging percentage |
| `teamStats.batting.ops` | String | On-base plus slugging |
| `teamStats.batting.stolenBases` | Integer | Stolen bases |
| `teamStats.batting.caughtStealing` | Integer | Caught stealing |
| `teamStats.batting.sacBunts` | Integer | Sacrifice bunts |
| `teamStats.batting.sacFlies` | Integer | Sacrifice flies |
| `teamStats.batting.groundOuts` | Integer | Ground outs |
| `teamStats.batting.flyOuts` | Integer | Fly outs |
| `teamStats.batting.lineOuts` | Integer | Line outs |

### Pitching Statistics
Complete team pitching statistics for the game:

| Field | Type | Description |
|-------|------|-------------|
| `teamStats.pitching.runs` | Integer | Runs allowed |
| `teamStats.pitching.earnedRuns` | Integer | Earned runs allowed |
| `teamStats.pitching.hits` | Integer | Hits allowed |
| `teamStats.pitching.homeRuns` | Integer | Home runs allowed |
| `teamStats.pitching.baseOnBalls` | Integer | Walks allowed |
| `teamStats.pitching.strikeOuts` | Integer | Strikeouts recorded |
| `teamStats.pitching.inningsPitched` | String | Innings pitched |
| `teamStats.pitching.era` | String | Team ERA for game |
| `teamStats.pitching.whip` | String | Walks + hits per inning |
| `teamStats.pitching.battersFaced` | Integer | Total batters faced |
| `teamStats.pitching.hitBatsmen` | Integer | Hit batsmen |
| `teamStats.pitching.wildPitches` | Integer | Wild pitches |
| `teamStats.pitching.balks` | Integer | Balks |
| `teamStats.pitching.groundOuts` | Integer | Ground outs induced |
| `teamStats.pitching.flyOuts` | Integer | Fly outs induced |
| `teamStats.pitching.lineOuts` | Integer | Line outs induced |

### Fielding Statistics
Team fielding statistics for the game:

| Field | Type | Description |
|-------|------|-------------|
| `teamStats.fielding.assists` | Integer | Fielding assists |
| `teamStats.fielding.putOuts` | Integer | Put outs |
| `teamStats.fielding.errors` | Integer | Fielding errors |
| `teamStats.fielding.chances` | Integer | Total chances |
| `teamStats.fielding.passedBalls` | Integer | Passed balls |
| `teamStats.fielding.doublePlays` | Integer | Double plays turned |
| `teamStats.fielding.triplePlays` | Integer | Triple plays turned |

## Player Data Structure

The `players` object contains detailed information for every player who participated in the game:

### Player Identification
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `players.ID{playerId}.person.id` | Integer | Unique player ID | 663853 |
| `players.ID{playerId}.person.fullName` | String | Player's full name | "Rafael Devers" |
| `players.ID{playerId}.person.link` | String | API link to player | "/api/v1/people/663853" |
| `players.ID{playerId}.jerseyNumber` | String | Jersey number | "11" |
| `players.ID{playerId}.person.boxscoreName` | String | Name for boxscore display | "Devers" |

### Position Information
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `players.ID{playerId}.position.code` | String | Position code | "5" |
| `players.ID{playerId}.position.name` | String | Position name | "Third Base" |
| `players.ID{playerId}.position.type` | String | Position type | "Infielder" |
| `players.ID{playerId}.position.abbreviation` | String | Position abbreviation | "3B" |

### Game Status
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `players.ID{playerId}.status.code` | String | Player status code | "A" |
| `players.ID{playerId}.status.description` | String | Player status | "Active" |
| `players.ID{playerId}.parentTeamId` | Integer | Team ID | 111 |
| `players.ID{playerId}.battingOrder` | String | Batting order position | "300" |

### Player Statistics
Each player contains detailed statistical data:

#### Batting Statistics (if applicable)
| Field | Type | Description |
|-------|------|-------------|
| `stats.batting.gamesPlayed` | Integer | Games played |
| `stats.batting.atBats` | Integer | At-bats |
| `stats.batting.runs` | Integer | Runs scored |
| `stats.batting.hits` | Integer | Hits |
| `stats.batting.doubles` | Integer | Doubles |
| `stats.batting.triples` | Integer | Triples |
| `stats.batting.homeRuns` | Integer | Home runs |
| `stats.batting.rbi` | Integer | RBIs |
| `stats.batting.baseOnBalls` | Integer | Walks |
| `stats.batting.strikeOuts` | Integer | Strikeouts |
| `stats.batting.stolenBases` | Integer | Stolen bases |
| `stats.batting.caughtStealing` | Integer | Caught stealing |
| `stats.batting.avg` | String | Batting average |
| `stats.batting.obp` | String | On-base percentage |
| `stats.batting.slg` | String | Slugging percentage |
| `stats.batting.ops` | String | OPS |

#### Pitching Statistics (if applicable)
| Field | Type | Description |
|-------|------|-------------|
| `stats.pitching.gamesPlayed` | Integer | Games pitched |
| `stats.pitching.gamesStarted` | Integer | Games started |
| `stats.pitching.wins` | Integer | Wins |
| `stats.pitching.losses` | Integer | Losses |
| `stats.pitching.saves` | Integer | Saves |
| `stats.pitching.saveOpportunities` | Integer | Save opportunities |
| `stats.pitching.holds` | Integer | Holds |
| `stats.pitching.inningsPitched` | String | Innings pitched |
| `stats.pitching.hits` | Integer | Hits allowed |
| `stats.pitching.runs` | Integer | Runs allowed |
| `stats.pitching.earnedRuns` | Integer | Earned runs |
| `stats.pitching.homeRuns` | Integer | Home runs allowed |
| `stats.pitching.baseOnBalls` | Integer | Walks |
| `stats.pitching.strikeOuts` | Integer | Strikeouts |
| `stats.pitching.era` | String | ERA |
| `stats.pitching.whip` | String | WHIP |

#### Fielding Statistics (if applicable)
| Field | Type | Description |
|-------|------|-------------|
| `stats.fielding.assists` | Integer | Fielding assists |
| `stats.fielding.putOuts` | Integer | Put outs |
| `stats.fielding.errors` | Integer | Fielding errors |
| `stats.fielding.chances` | Integer | Total chances |
| `stats.fielding.fielding` | String | Fielding percentage |

## Game Organization Arrays

### Batters Array
Lists player IDs of batters who appeared in the game:
```json
"batters": [680776, 646240, 608324, 671213, 596115]
```

### Pitchers Array
Lists player IDs of pitchers who appeared in the game:
```json
"pitchers": [656557, 677161, 458677, 686580, 676477]
```

### Bench Array
Lists player IDs of bench players:
```json
"bench": [663853, 666152, 608701, 657136]
```

### Bullpen Array
Lists player IDs of bullpen pitchers:
```json
"bullpen": [657514, 621111, 547973, 681867, 676979]
```

### Batting Order Array
Lists player IDs in batting order sequence:
```json
"battingOrder": [680776, 646240, 608324, 671213, 596115]
```

## Game Officials

Information about game officials (umpires):

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `officials[].official.id` | Integer | Umpire ID | 554242 |
| `officials[].official.fullName` | String | Umpire name | "Edwin Moscoso" |
| `officials[].official.link` | String | API link | "/api/v1/people/554242" |
| `officials[].officialType` | String | Umpire position | "Home Plate" |

### Official Types
- "Home Plate" - Home plate umpire
- "First Base" - First base umpire  
- "Second Base" - Second base umpire
- "Third Base" - Third base umpire

## Game Information

Comprehensive game details and conditions:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `info[].label` | String | Information category | "Weather" |
| `info[].value` | String | Information value | "71 degrees, Overcast." |

### Common Information Categories
- **Weather**: Game weather conditions
- **Wind**: Wind speed and direction
- **First pitch**: Game start time
- **T**: Game duration
- **Att**: Attendance figure
- **Venue**: Stadium name
- **Date**: Game date
- **Umpires**: Complete umpire crew
- **HBP**: Hit by pitch incidents
- **IBB**: Intentional walks
- **WP**: Wild pitches
- **Balk**: Balk calls
- **Pitches-strikes**: Pitch counts for all pitchers
- **Groundouts-flyouts**: Ground/fly out ratios
- **Batters faced**: Batters faced by each pitcher
- **Inherited runners-scored**: Relief pitcher inheritance stats

## Pitching Notes

Special pitching situations and notes:
```json
"pitchingNotes": [
  "Houck pitched to 1 batter in the 5th."
]
```

## Top Performers

Highlights of standout performances:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `topPerformers[].player.person.id` | Integer | Player ID | 608324 |
| `topPerformers[].player.person.boxscoreName` | String | Player name | "Bregman" |
| `topPerformers[].type` | String | Performance type | "hitter" |
| `topPerformers[].gameScore` | Integer | Game score rating | 70 |
| `topPerformers[].hittingGameScore` | Integer | Hitting game score | 70 |
| `topPerformers[].pitchingGameScore` | Integer | Pitching game score | 72 |

### Performance Types
- **"hitter"** - Outstanding hitting performance
- **"starter"** - Starting pitcher performance
- **"pitcher"** - Relief pitcher performance

## Team Notes

Special situations and substitutions:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `teams.away.note[].label` | String | Note category | "PH" |
| `teams.away.note[].value` | String | Note description | "Singled for Martini in the 9th." |
| `teams.away.info[].label` | String | Info category | "BATTING" |
| `teams.away.info[].value` | String | Info description | "2B: Devers (3, Morton)" |

## Data Quality and Completeness

### Available Data Points
- **Complete Player Statistics**: Every player's game performance
- **Real-time Updates**: Statistics update during game progress
- **Historical Context**: Season statistics alongside game stats
- **Comprehensive Coverage**: All positions, substitutions, and special plays

### Data Reliability
- **Source**: Official MLB Stats API
- **Accuracy**: Real-time official scoring
- **Completeness**: 100% coverage of game events
- **Timeliness**: Updated in real-time during games

## Usage Examples

### Common Data Extraction Patterns

1. **Team Performance Analysis**:
   - Extract team batting/pitching statistics
   - Compare home vs away performance
   - Analyze win/loss correlation with stats

2. **Player Performance Tracking**:
   - Individual player game statistics
   - Season progression analysis
   - Position-specific performance metrics

3. **Game Context Analysis**:
   - Weather impact on performance
   - Venue effects on scoring
   - Umpire crew analysis

4. **Advanced Analytics**:
   - Calculate team efficiency metrics
   - Player value in specific situations
   - Bullpen usage patterns

## File Locations

- **JSON Source**: `data/json/boxscores/mlb_boxscores_{date}.json`
- **Processed CSV**: `data/csv/boxscores/mlb_boxscores_{date}.csv`
- **Combined Data**: `data/csv/boxscores/combined_boxscores.csv`

This comprehensive structure provides the foundation for detailed baseball analytics, player evaluation, and game analysis across all aspects of MLB gameplay.