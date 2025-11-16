# MLB Data Pipeline - Product Requirements Document (PRD)

## Executive Summary

This document outlines the requirements for building an automated data pipeline that collects MLB game schedules and boxscore data. The pipeline will continuously monitor game schedules, track game status, and collect detailed boxscore information when games are completed.

## 1. Project Overview

### 1.1 Purpose
Develop a robust, automated data pipeline that:
- Fetches and maintains up-to-date MLB game schedules
- Monitors game status in real-time
- Collects comprehensive boxscore data when games reach "Final" status
- Provides reliable data storage and retrieval mechanisms

### 1.2 Business Objectives
- **Data Completeness**: Ensure 100% capture of scheduled games and their final boxscores
- **Data Timeliness**: Collect boxscore data within 30 minutes of game completion
- **Data Quality**: Maintain consistent, validated data structures
- **System Reliability**: Achieve 99.5% uptime for data collection processes
- **Cost Efficiency**: Minimize API calls while maintaining data freshness

### 1.3 Success Metrics
- Zero missing games in schedule data
- ≤30 minute latency for boxscore collection after game completion
- <1% data validation errors
- 99.5% pipeline uptime
- Daily automated data quality reports

## 2. Functional Requirements

### 2.1 Schedule Management

#### 2.1.1 Schedule Collection
- **Requirement**: Automatically fetch MLB game schedules for current and future dates
- **Frequency**: Daily at 6:00 AM EST
- **Data Source**: MLB Stats API (`/api/v1/schedule`)
- **Date Range**: Current date + next 7 days
- **Output Format**: JSON files stored as `mlb_games_YYYY-MM-DD.json`
- **Storage Location**: `data/json/games/`

#### 2.1.2 Schedule Updates
- **Requirement**: Handle schedule changes (postponements, time changes, cancellations)
- **Trigger**: Compare new schedule data with existing data
- **Actions**:
  - Update game times
  - Mark postponed games
  - Add makeup games
  - Log all schedule changes
- **Notification**: Send alerts for significant schedule changes

#### 2.1.3 Historical Schedule Maintenance
- **Requirement**: Maintain historical schedule data integrity
- **Retention**: Keep all schedule data (no deletion)
- **Validation**: Daily verification against stored boxscore data
- **Cleanup**: Archive data older than current season + 2 years

### 2.2 Game Status Monitoring

#### 2.2.1 Real-time Status Tracking
- **Requirement**: Monitor game status throughout the day
- **Frequency**: Every 15 minutes during active game periods (11 AM - 2 AM EST)
- **Monitored States**:
  - `Scheduled` - Game not yet started
  - `Pre-Game` - Game about to start
  - `In Progress` - Game in progress
  - `Final` - Game completed
  - `Postponed` - Game postponed
  - `Cancelled` - Game cancelled
- **Data Source**: MLB Stats API game status endpoints
- **Storage**: Update game status in schedule files and maintain status log

#### 2.2.2 Final Game Detection
- **Requirement**: Immediately detect when games reach "Final" status
- **Trigger**: Game status changes to "Final" or "Final/Completed"
- **Action**: Queue game for boxscore collection
- **Validation**: Verify final score is available and non-zero (except for rare cases)
- **Retry Logic**: Retry status check up to 3 times with 5-minute intervals

### 2.3 Boxscore Data Collection

#### 2.3.1 Boxscore Retrieval
- **Requirement**: Collect comprehensive boxscore data for completed games
- **Trigger**: Game status = "Final"
- **Delay**: Wait 10 minutes after final status to ensure data completeness
- **Data Source**: MLB Stats API (`/api/v1/game/{gamePk}/boxscore`)
- **Output Format**: JSON files stored as `mlb_boxscores_YYYY-MM-DD.json`
- **Storage Location**: `data/json/boxscores/`

#### 2.3.2 Boxscore Data Structure
- **Required Elements**:
  - Game metadata (gamePk, date, teams, venue)
  - Team statistics (batting, pitching, fielding)
  - Individual player statistics
  - Game officials
  - Game conditions (weather, attendance)
  - Scoring plays and key events
  - Top performers

#### 2.3.3 Data Validation
- **Requirement**: Validate boxscore data completeness and accuracy
- **Validation Rules**:
  - All starting players have statistics
  - Team totals match sum of individual player stats
  - Final scores match game outcome
  - Required metadata fields are present
  - No duplicate player entries
- **Error Handling**: Log validation errors and retry collection if critical data missing

### 2.4 Data Processing and Storage

#### 2.4.1 CSV Export Generation
- **Requirement**: Generate flattened CSV files for analytics
- **Source**: JSON boxscore data
- **Output Files**:
  - `mlb_boxscores_YYYY-MM-DD.csv` - Player-level batting statistics
  - `game_schedule.csv` - Complete schedule with outcomes
- **Storage Location**: `data/csv/boxscores/` and `data/`
- **Update Frequency**: After each new boxscore collection

#### 2.4.2 Data Aggregation
- **Requirement**: Maintain combined datasets
- **Combined Files**:
  - `combined_boxscores.csv` - All player statistics across dates
  - `combined_games.csv` - All game data across dates
- **Update Strategy**: Append new data to existing combined files
- **Deduplication**: Ensure no duplicate game entries

## 3. Technical Requirements

### 3.1 API Integration

#### 3.1.1 MLB Stats API
- **Base URL**: `https://statsapi.mlb.com`
- **Rate Limits**: Respect API rate limits (implement exponential backoff)
- **Authentication**: No authentication required for public endpoints
- **Error Handling**: Implement retry logic for 5xx errors, respect 429 rate limiting
- **Monitoring**: Log all API calls with response times and status codes

#### 3.1.2 Data Sources
- **Schedule Endpoint**: `/api/v1/schedule?sportId=1&startDate={date}&endDate={date}`
- **Live Game Data**: `/api/v1/schedule?sportId=1&date={date}&hydrate=game(content(summary,media(epg)),tickets),decisions`
- **Boxscore Endpoint**: `/api/v1/game/{gamePk}/boxscore`
- **Game Status**: `/api/v1/game/{gamePk}/feed/live` (for detailed status)

### 3.2 Infrastructure Requirements

#### 3.2.1 Compute Resources
- **Environment**: Python 3.9+
- **Memory**: Minimum 2GB RAM
- **Storage**: 10GB for current season data, 50GB for historical data
- **CPU**: Single core sufficient for current load

#### 3.2.2 Dependencies
- **Core Libraries**:
  - `requests` - HTTP API calls
  - `pandas` - Data manipulation and CSV generation
  - `json` - JSON data handling
  - `datetime` - Date/time operations
  - `logging` - Application logging
  - `schedule` - Task scheduling
  - `pathlib` - File system operations

#### 3.2.3 Scheduling
- **Scheduler**: Use `schedule` library or cron jobs
- **Schedule Tasks**:
  - Daily schedule fetch: 6:00 AM EST
  - Game status monitoring: Every 15 minutes (11 AM - 2 AM EST)
  - Boxscore collection: Triggered by final game status
  - Data validation: Daily at 3:00 AM EST
  - Log rotation: Weekly

### 3.3 Data Storage Structure

#### 3.3.1 Directory Structure
```
data/
├── json/
│   ├── games/
│   │   └── mlb_games_YYYY-MM-DD.json
│   └── boxscores/
│       └── mlb_boxscores_YYYY-MM-DD.json
├── csv/
│   ├── games/
│   │   └── combined_games.csv
│   └── boxscores/
│       ├── mlb_boxscores_YYYY-MM-DD.csv
│       └── combined_boxscores.csv
└── logs/
    ├── pipeline.log
    ├── api_calls.log
    └── data_validation.log
```

#### 3.3.2 File Naming Conventions
- **Date Format**: `YYYY-MM-DD` (ISO 8601)
- **Game Files**: `mlb_games_YYYY-MM-DD.json`
- **Boxscore Files**: `mlb_boxscores_YYYY-MM-DD.json`
- **CSV Files**: `mlb_boxscores_YYYY-MM-DD.csv`
- **Log Files**: `{component}_{YYYY-MM-DD}.log`

## 4. Non-Functional Requirements

### 4.1 Performance

#### 4.1.1 Response Time
- **API Calls**: Maximum 10 seconds timeout
- **Data Processing**: Complete daily processing within 30 minutes
- **File Operations**: CSV generation within 5 minutes per day's data

#### 4.1.2 Throughput
- **Concurrent API Calls**: Maximum 2 concurrent requests
- **Daily Volume**: Handle 15-20 games per day (peak load)
- **Batch Processing**: Process up to 50 games in single batch

### 4.2 Reliability

#### 4.2.1 Error Handling
- **API Failures**: Retry up to 3 times with exponential backoff
- **Network Issues**: Queue failed requests for retry
- **Data Corruption**: Validate data before saving, rollback on errors
- **System Failures**: Resume from last successful checkpoint

#### 4.2.2 Monitoring
- **Health Checks**: Daily pipeline health verification
- **Alerting**: Email notifications for critical failures
- **Metrics**: Track API success rates, data completeness, processing times
- **Logging**: Comprehensive logging at INFO, WARN, and ERROR levels

### 4.3 Security

#### 4.3.1 Data Protection
- **Access Control**: Read-only access to source data
- **Data Integrity**: Checksum validation for critical files
- **Backup Strategy**: Daily backups of JSON files

#### 4.3.2 API Security
- **Rate Limiting**: Implement client-side rate limiting
- **User Agent**: Identify requests with appropriate user agent
- **Error Handling**: Don't expose internal errors in logs

## 5. Implementation Plan

### 5.1 Phase 1: Core Pipeline (Week 1-2)
- [ ] Basic schedule collection script
- [ ] JSON file storage implementation
- [ ] Game status monitoring loop
- [ ] Basic boxscore collection
- [ ] Error logging framework

### 5.2 Phase 2: Data Processing (Week 3)
- [ ] CSV export functionality
- [ ] Data validation rules
- [ ] Combined dataset maintenance
- [ ] File organization and cleanup

### 5.3 Phase 3: Reliability & Monitoring (Week 4)
- [ ] Comprehensive error handling
- [ ] Retry mechanisms
- [ ] Health monitoring
- [ ] Alerting system
- [ ] Performance optimization

### 5.4 Phase 4: Automation & Scheduling (Week 5)
- [ ] Automated scheduling setup
- [ ] Production deployment
- [ ] Monitoring dashboard
- [ ] Documentation completion
- [ ] User acceptance testing

## 6. Risk Assessment

### 6.1 Technical Risks
- **API Changes**: MLB may modify API structure
  - *Mitigation*: Version API calls, implement change detection
- **Rate Limiting**: Exceeding API rate limits
  - *Mitigation*: Implement conservative rate limiting, monitoring
- **Data Volume**: Storage requirements may exceed capacity
  - *Mitigation*: Implement data archiving strategy

### 6.2 Operational Risks
- **Schedule Changes**: Late schedule modifications
  - *Mitigation*: Frequent schedule refreshes, change detection
- **Extended Games**: Extra-inning games affecting timing
  - *Mitigation*: Flexible scheduling, extended monitoring windows
- **System Downtime**: Infrastructure failures during games
  - *Mitigation*: Robust error handling, recovery procedures

## 7. Success Criteria

### 7.1 Data Quality Metrics
- [ ] 100% of scheduled games captured
- [ ] 99%+ of final games have boxscores within 30 minutes
- [ ] <1% data validation errors
- [ ] Zero data loss incidents

### 7.2 System Performance
- [ ] 99.5% uptime during game periods
- [ ] <10 second average API response time
- [ ] <5 minute daily data processing time
- [ ] Successful automated scheduling for 30+ consecutive days

### 7.3 Operational Excellence
- [ ] Automated alerting functional
- [ ] Comprehensive documentation complete
- [ ] Recovery procedures tested
- [ ] Performance monitoring dashboard operational

## 8. Appendices

### 8.1 API Endpoints Reference
- **Schedule**: `https://statsapi.mlb.com/api/v1/schedule?sportId=1`
- **Boxscore**: `https://statsapi.mlb.com/api/v1/game/{gamePk}/boxscore`
- **Live Feed**: `https://statsapi.mlb.com/api/v1/game/{gamePk}/feed/live`

### 8.2 Sample Data Structures
See existing files:
- `data/json/games/mlb_games_2025-07-18.json`
- `data/json/boxscores/mlb_boxscores_2025-07-18.json`
- `data/csv/boxscores/mlb_boxscores_2025-07-18.csv`

### 8.3 Error Codes and Handling
- **200**: Success - Process normally
- **429**: Rate Limited - Implement exponential backoff
- **500-503**: Server Error - Retry up to 3 times
- **404**: Not Found - Log and skip (game may not exist yet)

---

**Document Version**: 1.0  
**Last Updated**: November 16, 2025  
**Author**: MLB Data Pipeline Team  
**Review Date**: December 1, 2025