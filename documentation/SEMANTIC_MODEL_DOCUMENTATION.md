# MLB Data - Semantic Model Documentation

## 📋 **Executive Summary**

This document provides comprehensive documentation for the MLB Data Power BI semantic model, designed to track and analyze Major League Baseball player performance, game schedules, and team statistics. The model follows industry best practices for Power BI development with a star schema architecture optimized for analytical queries.

**Last Updated**: November 28, 2025  
**Model Name**: Model  
**Data Coverage**: 2025 MLB Season (March 27 - September 30)  
**Total Games**: ~2,430 games (81-82 per team)

---

## 🎯 **Model Purpose & Business Objectives**

### Primary Use Cases
1. **Player Performance Analysis** - Track individual batting statistics across games and seasons
2. **Team Performance Comparison** - Analyze team offensive production and trends
3. **Game-Level Analytics** - Detailed game outcomes and contextual information
4. **Sabermetric Calculations** - Advanced baseball statistics (OPS, OBP, SLG)
5. **Historical Trend Analysis** - Performance patterns over time

### Key Stakeholders
- Baseball analysts and scouts
- Team management and coaching staff
- Sports media and journalists
- Fantasy baseball enthusiasts
- Data scientists and researchers

---

## 🏗️ **Model Architecture**

### **Schema Design**: Star Schema
The model implements a **star schema** for optimal query performance:
- **1 Fact Table**: Player Hitting (batting statistics per game)
- **3 Dimension Tables**: Player Info, Game Schedule, Date
- **Data Grain**: One row per player per game batting performance

### **Model Configuration**
- **Default Mode**: Import
- **Culture**: en-US (English - United States)
- **Data Source Version**: PowerBI_V3
- **Time Intelligence**: Enabled (dedicated Date dimension table)
- **Refresh Strategy**: Full refresh from CSV source files

---

## 📊 **Tables Structure**

### **1. Player Hitting** (Fact Table)
**Purpose**: Core fact table containing player batting statistics for each game appearance

**Row Count**: ~98,000+ rows  
**Grain**: Player + Game (one row per player per game)  
**Refresh Frequency**: After each game batch processing

#### **Key Columns** (42 total)
| Column Name | Data Type | Description | Business Use |
|-------------|-----------|-------------|--------------|
| `gamePk` | Int64 | Unique game identifier (FK) | Links to Game Schedule |
| `player_id` | Int64 | Unique player identifier (FK) | Links to Player Info |
| `team` | Text | Team name | Team grouping |
| `team_type` | Text | Home/Away designation | Home field advantage analysis |
| `player_name` | Text | Player full name | Display purposes |
| `batting_order` | Int64 | Position in batting order (1-9) | Lineup analysis |
| `position` | Text | Defensive position name | Position-based comparisons |
| `position_code` | Int64 | Numeric position code | Filtering/grouping |
| `date` | Date | Game date | Time-based analysis |
| **Batting Statistics** ||||
| `atBats` | Int64 | Official at-bats | Denominator for batting average |
| `hits` | Int64 | Total hits | Numerator for batting average |
| `runs` | Int64 | Runs scored | Run production |
| `homeRuns` | Int64 | Home runs hit | Power metric |
| `rbi` | Int64 | Runs batted in | Run production |
| `doubles` | Int64 | Two-base hits | Extra-base hit tracking |
| `triples` | Int64 | Three-base hits | Speed/power indicator |
| `baseOnBalls` | Int64 | Walks (BB) | Plate discipline |
| `strikeOuts` | Int64 | Strikeouts (K) | Contact ability |
| `stolenBases` | Int64 | Successful steals (SB) | Base running |
| `caughtStealing` | Int64 | Caught stealing (CS) | Base running risk |
| `hitByPitch` | Int64 | Hit by pitch (HBP) | Plate appearance outcomes |
| `sacFlies` | Int64 | Sacrifice flies | Situational hitting |
| `plateAppearances` | Int64 | Total plate appearances | Volume metric |
| `totalBases` | Int64 | Total bases from hits | Power/productivity |
| `leftOnBase` | Int64 | Runners left on base | Situational context |
| **Out Types** ||||
| `flyOuts` | Int64 | Outs on fly balls | Batted ball profile |
| `groundOuts` | Int64 | Outs on ground balls | Batted ball profile |
| `airOuts` | Int64 | Outs in the air | Combined fly/pop outs |
| `popOuts` | Int64 | Infield pop outs | Weak contact |
| `lineOuts` | Int64 | Line drive outs | Hard contact outs |

#### **Measures** (27 total)
| Measure | Formula | Description | Format |
|---------|---------|-------------|--------|
| `H` | SUM([hits]) | Total hits | #,##0 |
| `AB` | SUM([atBats]) | Total at-bats | #,##0 |
| `R` | SUM([runs]) | Total runs scored | #,##0 |
| `HR` | SUM([homeRuns]) | Total home runs | #,##0 |
| `RBIs` | SUM([rbi]) | Total runs batted in | #,##0 |
| `2B` | SUM([doubles]) | Total doubles | #,##0 |
| `3B` | SUM([triples]) | Total triples | #,##0 |
| `BB` | SUM([baseOnBalls]) | Total walks | #,##0 |
| `SO` | SUM([strikeOuts]) | Total strikeouts | #,##0 |
| `SB` | SUM([stolenBases]) | Total stolen bases | #,##0 |
| `CS` | SUM([caughtStealing]) | Caught stealing | #,##0 |
| `PA` | SUM([plateAppearances]) | Plate appearances | #,##0 |
| `TB` | SUM([totalBases]) | Total bases | #,##0 |
| `AVG` | DIVIDE([H], [AB]) | Batting average | 0.000 |
| `OBP` | (Hits + Walks + HBP) / PA | On-base percentage | 0.000 |
| `SLG` | TB / AB | Slugging percentage | 0.000 |
| `OPS` | OBP + SLG | On-base plus slugging | 0.000 |
| `G` | DISTINCTCOUNT([gamePk]) | Games played | #,##0 |
| `FO` | SUM([flyOuts]) | Fly outs | #,##0 |
| `GO` | SUM([groundOuts]) | Ground outs | #,##0 |
| `AO` | SUM([airOuts]) | Air outs | #,##0 |

**Data Source**: `mlb_player_batting_boxscores_2025-03-27_to_2025-09-30.csv`  
**Lineage Tag**: 8b80e307-77cd-4bd6-8649-7d4b173456a1

---

### **2. Player Info** (Dimension Table)
**Purpose**: Comprehensive player biographical and physical attributes

**Row Count**: ~1,500+ players  
**Type**: Type 1 Slowly Changing Dimension (current state only)

#### **Key Columns** (46 total)
| Column Name | Data Type | Description | Business Use |
|-------------|-----------|-------------|--------------|
| `id` | Int64 | Unique player ID (PK) | Primary identifier |
| `Player` | Text | Full player name | Display name |
| `firstName` | Text | First name | Name parsing |
| `lastName` | Text | Last name | Sorting/grouping |
| `primaryNumber` | Text | Jersey number | Player identification |
| `birthDate` | Date | Date of birth | Age calculations |
| `currentAge` | Int64 | Current age | Age-based analysis |
| `height` | Text | Height (e.g., "6' 2\"") | Physical attributes |
| `weight` | Int64 | Weight in pounds | Physical attributes |
| `birthCity` | Text | Birth city | Geographic analysis |
| `birthCountry` | Text | Birth country | International players |
| `active` | Boolean | Active status | Current roster |
| `mlbDebutDate` | Date | MLB debut date | Experience calculation |
| `primaryPosition.code` | Text | Position code | Position filtering |
| `primaryPosition.name` | Text | Position name | Display purposes |
| `primaryPosition.type` | Text | Position type category | Infielder/Outfielder/etc. |
| `P` | Text | Position abbreviation | Short display |
| `batSide.code` | Text | Batting side (L/R/S) | Platoon analysis |
| `batSide.description` | Text | Batting side description | Handedness analysis |
| `pitchHand.code` | Text | Throwing hand (L/R) | If player pitches |
| `pitchHand.description` | Text | Throwing description | Handedness |

**Data Source**: `player_info.csv`  
**Lineage Tag**: 5a117058-adfd-46c0-a4db-e3b17ec6446e

---

### **3. Game Schedule** (Dimension Table)
**Purpose**: Complete game schedule with outcomes, venue, and contextual information

**Row Count**: ~2,430 games  
**Grain**: One row per scheduled game

#### **Key Columns** (65 total)
| Column Name | Data Type | Description | Business Use |
|-------------|-----------|-------------|--------------|
| `gamePk` | Int64 | Unique game ID (PK) | Primary identifier |
| `gameDate` | DateTime | Game date and time | Scheduling |
| `officialDate` | Date | Official game date | Grouping/filtering |
| `season` | Int64 | Season year (2025) | Season filtering |
| `gameType` | Text | Game type (R/P/S/E) | Regular/Playoff/Spring |
| `dayNight` | Text | Day/Night game | Time of day analysis |
| **Away Team** ||||
| `teams.away.team.id` | Int64 | Away team ID | Team identification |
| `teams.away.team.name` | Text | Away team name | Display purposes |
| `teams.away.score` | Int64 | Away team final score | Game outcome |
| `teams.away.isWinner` | Boolean | Away team won | Win/loss tracking |
| `teams.away.leagueRecord.wins` | Int64 | Season wins (at game time) | Win-loss record |
| `teams.away.leagueRecord.losses` | Int64 | Season losses | Win-loss record |
| `teams.away.leagueRecord.pct` | Decimal | Winning percentage | Team strength |
| **Home Team** ||||
| `teams.home.team.id` | Int64 | Home team ID | Team identification |
| `teams.home.team.name` | Text | Home team name | Display purposes |
| `teams.home.score` | Int64 | Home team final score | Game outcome |
| `teams.home.isWinner` | Boolean | Home team won | Win/loss tracking |
| `teams.home.leagueRecord.wins` | Int64 | Season wins | Win-loss record |
| `teams.home.leagueRecord.losses` | Int64 | Season losses | Win-loss record |
| `teams.home.leagueRecord.pct` | Decimal | Winning percentage | Team strength |
| **Game Details** ||||
| `venue.id` | Int64 | Venue ID | Venue identification |
| `venue.name` | Text | Stadium/park name | Venue analysis |
| `status.detailedState` | Text | Game status | Final/In Progress/etc. |
| `status.abstractGameState` | Text | State category | Preview/Live/Final |
| `gamesInSeries` | Int64 | Number of games in series | Series context |
| `seriesGameNumber` | Int64 | Game number in series | Series progression |
| `seriesDescription` | Text | Series description | Series type |
| `doubleHeader` | Text | Doubleheader designation | Scheduling context |
| `scheduledInnings` | Int64 | Scheduled innings (9) | Game length |

#### **Measures** (1 total)
| Measure | Formula | Description |
|---------|---------|-------------|
| `Games` | COUNTROWS('Game Schedule') | Count of games |

**Data Source**: `game-schedule-combined.csv`  
**Lineage Tag**: 0f340865-ab89-4b21-8f32-79330d98a8ea

---

### **4. Date** (Dimension Table)
**Purpose**: Dedicated date dimension for time intelligence calculations and temporal analysis

**Row Count**: 306 dates (March 1 - December 31, 2025)  
**Type**: Date Dimension (auto-generated via M script)

#### **Key Columns** (11 total)
| Column Name | Data Type | Description | Business Use |
|-------------|-----------|-------------|--------------|
| `Date` | Date | Calendar date (PK) | Primary date identifier |
| `Year` | Int64 | Year number | Year filtering (2025) |
| `Quarter` | Int64 | Quarter number (1-4) | Quarterly analysis |
| `Month` | Int64 | Month number (1-12) | Monthly grouping |
| `MonthName` | Text | Full month name | Display purposes |
| `Day` | Int64 | Day of month (1-31) | Daily analysis |
| `DayOfWeek` | Int64 | Day of week (1=Mon, 7=Sun) | Weekday analysis |
| `DayName` | Text | Full day name | Display purposes |
| `WeekOfYear` | Int64 | ISO week number (1-53) | Weekly analysis |
| `YearMonth` | Text | YYYY-MM format (e.g., 2025-03) | Month sorting/grouping |
| `YearQuarter` | Text | Display format (e.g., 2025 Q1) | Quarter display |

**Key Features**:
- Continuous date range covering entire MLB season
- ISO 8601 week numbering (weeks start Monday)
- Sortable YearMonth for chronological ordering
- No gaps in date sequence (includes off-days)

**M Expression**: Auto-generated using Power Query with Date.* functions
```powerquery
// Generate dates from March 1 to December 31, 2025
StartDate = #date(2025, 3, 1)
EndDate = #date(2025, 12, 31)
NumberOfDays = Duration.Days(EndDate - StartDate) + 1
DateList = List.Dates(StartDate, NumberOfDays, #duration(1, 0, 0, 0))
```

**Usage**:
- **Mark as Date Table**: Right-click table > "Mark as Date Table" in Power BI Desktop
- **Relationship**: Link to `Player Hitting[date]` for time intelligence
- **Time Intelligence Functions**: Enables DATESYTD, DATEADD, SAMEPERIODLASTYEAR, etc.

---

## 🔗 **Relationships**

### **Relationship 1: Player Hitting ↔ Game Schedule**
- **Type**: Many-to-One
- **From**: Player Hitting[gamePk]
- **To**: Game Schedule[gamePk]
- **Cardinality**: Many (Player Hitting) to One (Game Schedule)
- **Cross Filter Direction**: Both Directions (Bidirectional)
- **Active**: Yes
- **Purpose**: Links batting statistics to game context (date, teams, venue)
- **Business Logic**: Multiple players participate in each game

### **Relationship 2: Player Hitting ↔ Player Info**
- **Type**: Many-to-One
- **From**: Player Hitting[player_id]
- **To**: Player Info[id]
- **Cardinality**: Many (Player Hitting) to One (Player Info)
- **Cross Filter Direction**: Single (One Direction)
- **Active**: Yes
- **Purpose**: Links batting performances to player biographical data
- **Business Logic**: Each player has multiple game performances

### **Relationship 3: Player Hitting ↔ Date** (Recommended)
- **Type**: Many-to-One
- **From**: Player Hitting[date]
- **To**: Date[Date]
- **Cardinality**: Many (Player Hitting) to One (Date)
- **Cross Filter Direction**: Single (One Direction)
- **Active**: Yes
- **Purpose**: Enables time intelligence calculations and temporal filtering
- **Business Logic**: Multiple player performances occur on each date
- **Setup Required**: This relationship should be created in Power BI Desktop

**Relationship Diagram**:
```
Player Info (Dimension)         Date (Dimension)
    |                               |
    | 1:Many (player_id)            | 1:Many (date)
    |                               |
    └─────→ Player Hitting (Fact) ←─┘
                   ↕
         Many:1 (gamePk, bidirectional)
                   |
         Game Schedule (Dimension)
```

---

## 📈 **Key Measures & Calculations**

### **Basic Statistics**
These measures aggregate raw statistical totals:
- **H** (Hits): Total successful hits
- **AB** (At Bats): Total official at-bats
- **R** (Runs): Total runs scored
- **HR** (Home Runs): Total home runs
- **RBIs**: Total runs batted in

### **Rate Statistics**
Advanced metrics for performance evaluation:

#### **Batting Average (AVG)**
```dax
AVG = DIVIDE([H], [AB])
```
**Description**: Hits divided by at-bats, the fundamental batting success rate  
**Format**: 0.000 (e.g., 0.275)  
**League Average**: ~0.245

#### **On-Base Percentage (OBP)**
```dax
OBP = DIVIDE([H] + [BB] + [HBP], [PA])
```
**Description**: Rate at which a batter reaches base via hit, walk, or HBP  
**Format**: 0.000  
**League Average**: ~0.315

#### **Slugging Percentage (SLG)**
```dax
SLG = DIVIDE([TB], [AB])
```
**Description**: Total bases per at-bat, measuring power production  
**Format**: 0.000  
**League Average**: ~0.410

#### **On-Base Plus Slugging (OPS)**
```dax
OPS = [OBP] + [SLG]
```
**Description**: Combined measure of getting on base and hitting for power  
**Format**: 0.000  
**Benchmark**: 
- Elite: > 0.900
- Above Average: 0.750 - 0.900
- Average: 0.700 - 0.750
- Below Average: < 0.700

### **Time Intelligence Measures**
Enabled by the Date dimension table:

#### **Year-to-Date (YTD) Calculations**
```dax
Runs YTD = 
CALCULATE(
    [R],
    DATESYTD('Date'[Date])
)
```
**Description**: Cumulative runs from season start to current date  
**Use Case**: Season progress tracking

```dax
Hits YTD = 
CALCULATE(
    [H],
    DATESYTD('Date'[Date])
)
```

#### **Period Comparisons**
```dax
Runs Previous Month = 
CALCULATE(
    [R],
    DATEADD('Date'[Date], -1, MONTH)
)
```
**Description**: Runs scored in the previous month  
**Use Case**: Month-over-month trend analysis

```dax
Runs MoM % = 
VAR CurrentRuns = [R]
VAR PreviousRuns = [Runs Previous Month]
RETURN
DIVIDE(
    CurrentRuns - PreviousRuns,
    PreviousRuns
)
```
**Description**: Month-over-month growth percentage  
**Format**: 0.0%

#### **Rolling Averages**
```dax
Runs 7-Day Avg = 
CALCULATE(
    [R],
    DATESINPERIOD(
        'Date'[Date],
        LASTDATE('Date'[Date]),
        -7,
        DAY
    )
) / 7
```
**Description**: Moving average over last 7 days  
**Use Case**: Smoothing daily volatility, trend identification

```dax
Runs Last 30 Days = 
CALCULATE(
    [R],
    DATESINPERIOD(
        'Date'[Date],
        LASTDATE('Date'[Date]),
        -30,
        DAY
    )
)
```
**Description**: Total runs in last 30 days  
**Use Case**: Recent form analysis

#### **Quarter-to-Date (QTD)**
```dax
Runs QTD = 
CALCULATE(
    [R],
    DATESQTD('Date'[Date])
)
```
**Description**: Cumulative runs in current quarter  
**Use Case**: Quarterly performance tracking

#### **Same Period Comparisons**
```dax
Runs SPLY = 
CALCULATE(
    [R],
    SAMEPERIODLASTYEAR('Date'[Date])
)
```
**Description**: Runs in same period last year  
**Use Case**: Year-over-year comparison (requires multi-year data)

```dax
Runs vs SPLY = [R] - [Runs SPLY]
```
**Description**: Difference from same period last year

---

## 🎯 **Best Practices & Guidelines**

### **Data Modeling Best Practices**

#### ✅ **What We Did Right**
1. **Star Schema Design**: Clear fact-dimension separation for query performance
2. **Proper Relationships**: Correct cardinalities and filter directions
3. **Meaningful Measures**: Business-relevant calculations with proper formatting
4. **Descriptive Naming**: Clear, understandable column and measure names
5. **Data Types**: Appropriate data types for each column
6. **Lineage Tracking**: Lineage tags for source tracking and version control
7. **Date Dimension**: Dedicated Date table for time intelligence capabilities

#### ⚠️ **Optimization Opportunities**
1. ~~**Date Table**: Consider adding a dedicated Date dimension for enhanced time intelligence~~ ✅ **COMPLETED**
2. **Calculation Groups**: Could create calculation groups for time comparisons (YoY, QoQ)
3. **Field Parameters**: Enable dynamic measure selection in visuals
4. **Aggregations**: For large datasets, consider aggregation tables
5. **Incremental Refresh**: Implement for production to reduce refresh times
6. **Data Categories**: Set data categories for map visuals:
    - **City**: Set columns like `birthCity`, `venue.name` to "City"
    - **State/Province**: Set columns like `venue.state` (if present) to "State or Province"
    - **Country/Region**: Set columns like `birthCountry` to "Country/Region"
    - **Latitude/Longitude**: If available, set to "Latitude" and "Longitude"

    **How to set in Power BI Desktop:**
    1. Select the column in Data view or Model view
    2. Go to the Column tools ribbon
    3. Set the "Data Category" dropdown to the appropriate value (e.g., City, State, Country/Region)
    4. This improves map accuracy and geocoding in visuals

### **Measure Development Guidelines**

#### **Naming Conventions**
- **Abbreviations for Common Stats**: H, AB, HR, RBI (industry standard)
- **Full Names for Complex Metrics**: "Batting Average" not "BA"
- **Descriptions**: Always include measure descriptions for clarity

#### **DAX Best Practices**
```dax
// ✅ GOOD: Clear, efficient, handles blanks
AVG = DIVIDE([H], [AB], BLANK())

// ❌ AVOID: No blank handling, confusing
AVG = [H] / [AB]
```

#### **Format Strings**
- **Counting Stats**: #,##0 (e.g., 156 hits)
- **Rates/Averages**: 0.000 (e.g., 0.287 batting average)
- **Percentages**: 0.0% (e.g., 28.5% strikeout rate)

### **Performance Optimization**

#### **Query Performance Tips**
1. **Use DAX Variables**: Store intermediate calculations
2. **Avoid Calculated Columns**: Use measures when possible
3. **Filter Context**: Leverage relationship filters before explicit filters
4. **Minimize Bidirectional**: Use sparingly (currently one bidirectional relationship)

#### **Data Refresh Optimization**
- **Current**: Full refresh from CSV (~98K rows in fact table)
- **Recommended**: Implement incremental refresh by date
- **Strategy**: Refresh only recent games, archive historical data

---

## 📊 **Common Analysis Patterns**

### **Player Performance Analysis**
```dax
// Top 10 Batters by OPS (min 100 AB)
EVALUATE
TOPN(
    10,
    FILTER(
        ADDCOLUMNS(
            VALUES('Player Info'[Player]),
            "At Bats", [AB],
            "OPS", [OPS]
        ),
        [At Bats] >= 100
    ),
    [OPS], DESC
)
```

### **Team Performance Comparison**
```dax
// Team Offensive Production
EVALUATE
SUMMARIZE(
    'Game Schedule',
    'Game Schedule'[teams.away.team.name],
    "Total Runs", [R],
    "Total Hits", [H],
    "Home Runs", [HR],
    "Team AVG", [AVG],
    "Team OPS", [OPS]
)
ORDER BY [Total Runs] DESC
```

### **Home Field Advantage**
```dax
// Compare Home vs Away Performance
Home Runs (Home) = 
    CALCULATE(
        [R],
        'Player Hitting'[team_type] = "home"
    )

Home Runs (Away) = 
    CALCULATE(
        [R],
        'Player Hitting'[team_type] = "away"
    )

Home Field Advantage = [Home Runs (Home)] - [Home Runs (Away)]
```

---

## 🔍 **Data Quality & Validation**

### **Data Quality Checks**

#### **Completeness**
- ✅ All games have corresponding Player Hitting records
- ✅ All players in Player Hitting exist in Player Info
- ✅ No orphaned records in fact table

#### **Accuracy**
- ✅ Batting average calculations verified against source
- ✅ Team totals reconcile with individual player stats
- ✅ Date ranges match expected season dates

#### **Consistency**
- ✅ Consistent naming conventions across tables
- ✅ Data types aligned properly
- ✅ Relationships enforce referential integrity

### **Known Limitations**

1. **Single Season**: Currently contains only 2025 season data
2. **Batting Only**: No pitching statistics included
3. **No Defensive Stats**: Missing fielding metrics
4. **Static Player Info**: Player attributes don't track historical changes
5. **CSV Source**: Manual refresh required, not real-time

---

## 📁 **File Structure & Source Mapping**

### **PBIP Project Structure**
```
mlb-data/
├── mlb-data.pbip                          # Project shortcut file
├── mlb-data.SemanticModel/
│   ├── definition.pbism                    # Semantic model definition
│   ├── diagramLayout.json                  # Model diagram layout
│   ├── definition/
│   │   ├── database.tmdl                   # Database metadata
│   │   ├── model.tmdl                      # Model configuration
│   │   ├── relationships.tmdl              # Relationship definitions
│   │   └── tables/
│   │       ├── Player Hitting.tmdl         # Fact table definition
│   │       ├── Player Info.tmdl            # Player dimension
│   │       ├── Game Schedule.tmdl          # Game dimension
│   │       └── Date.tmdl                   # Date dimension (NEW)
│   └── DAXQueries/                         # Saved DAX queries
│       ├── Query 1.dax through Query 9.dax
└── mlb-data.Report/
    ├── definition.pbir                     # Report definition
    └── definition/
        ├── report.json                     # Report metadata
        └── pages/                          # Report pages
```

### **Data Source Files**
```
data/csv/
├── boxscores/
│   └── mlb_player_batting_boxscores_2025-03-27_to_2025-09-30.csv
├── players/
│   └── player_info.csv
└── games/
    └── game-schedule-combined.csv
```

---

## 🚀 **Usage Examples**

### **Report Building**

#### **Player Leaderboard**
1. Visual: Table
2. Columns: Player[Player], Position[primaryPosition.name]
3. Values: [G], [AB], [H], [HR], [RBI], [AVG], [OPS]
4. Filters: [AB] >= 200 (minimum at-bats)
5. Sort: [OPS] descending

#### **Team Comparison Matrix**
1. Visual: Matrix
2. Rows: Game Schedule[teams.away.team.name]
3. Values: [R], [H], [HR], [AVG], [SLG], [OPS]
4. Conditional Formatting: Color scale on [OPS]

#### **Time Series Analysis**
1. Visual: Line Chart
2. Axis: Date[Date]
3. Values: [AVG], [OBP], [SLG]
4. Legend: Player Info[Player]
5. Filters: Top 10 players by [AB]

#### **Month-over-Month Trend**
1. Visual: Clustered Column Chart
2. Axis: Date[YearMonth]
3. Values: [Runs MoM %], [R]
4. Secondary Axis: [Runs MoM %] (line)
5. Sort: By Date[YearMonth] ascending

#### **YTD Performance Dashboard**
1. Visual: Card (KPI)
2. Values: [Runs YTD], [Hits YTD], [HR]
3. Visual: Line Chart
4. Axis: Date[Date]
5. Values: [Runs YTD]
6. Conditional Formatting: Above/below target

---

## 🔄 **Maintenance & Updates**

### **Refresh Schedule**
- **Frequency**: After each batch of games processed
- **Method**: Manual refresh or scheduled refresh in Power BI Service
- **Duration**: ~30 seconds for current dataset size
- **Dependencies**: Updated CSV files in data folder

### **Version Control**
- **Repository**: Datamazin/mlb-data (GitHub)
- **Branch**: main
- **TMDL Format**: Enables source control for semantic model
- **Tracking**: Lineage tags track object changes

### **Change Management**
1. **Adding New Measures**: Document formula, description, and format
2. **Schema Changes**: Update this documentation
3. **Data Source Updates**: Verify data types and mappings
4. **Testing**: Validate calculations against known results

---

## 📞 **Support & Resources**

### **Documentation**
- **Boxscore Structure**: See `boxscore.md`
- **Game Schedule**: See `game-schedule.md`
- **Player Info**: See `PLAYER_INFO_ANALYSIS.md`
- **Data Pipeline**: See `MLB_Data_Pipeline_PRD.md`

### **External Resources**
- **MLB Stats API**: https://statsapi.mlb.com
- **Power BI Documentation**: https://learn.microsoft.com/power-bi
- **DAX Reference**: https://dax.guide
- **Baseball Reference**: https://www.baseball-reference.com

### **MCP Server Connection**
- **Connection Name**: "conntect to project"
- **Type**: Power BI Desktop (localhost:62038)
- **Tools Available**: Table operations, measure operations, DAX queries, relationship management

---

## 📝 **Appendix**

### **A. Data Dictionary - Complete Column List**

See individual table sections above for complete column listings.

### **B. Measure Reference**

Complete list of 28 measures with formulas available in model definition.

### **C. Baseball Statistics Glossary**

- **AB**: At Bats - Official plate appearances resulting in hit or out
- **AVG**: Batting Average - Hits divided by at-bats
- **BB**: Base on Balls (Walks) - Four balls outside strike zone
- **CS**: Caught Stealing - Failed stolen base attempt
- **H**: Hits - Ball put in play resulting in reaching base safely
- **HBP**: Hit By Pitch - Batter struck by pitched ball
- **HR**: Home Run - Four-base hit clearing the outfield fence
- **OBP**: On-Base Percentage - Rate of reaching base
- **OPS**: On-Base Plus Slugging - Combined OBP and SLG
- **PA**: Plate Appearances - All trips to the plate
- **RBI**: Runs Batted In - Runs scored due to batter's action
- **SB**: Stolen Base - Successful base advancement while pitcher delivers
- **SLG**: Slugging Percentage - Total bases per at-bat
- **SO/K**: Strikeout - Three strikes result in out
- **TB**: Total Bases - Sum of bases from all hits (1B=1, 2B=2, 3B=3, HR=4)

---

**Document Version**: 1.0  
**Created**: November 28, 2025  
**Author**: MLB Data Analytics Team  
**Next Review**: End of 2025 Season
