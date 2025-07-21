import pandas as pd
import pyodbc
import os
from sqlalchemy import create_engine

def create_boxscore_table():
    """Create the boxscore table if it doesn't exist"""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS dbo.boxscore_batting (
        id INT IDENTITY(1,1) PRIMARY KEY,
        gamePk INT,
        team NVARCHAR(100),
        team_type NVARCHAR(10),
        player_id INT,
        player_name NVARCHAR(100),
        batting_order INT,
        gamesPlayed INT,
        atBats INT,
        hits INT,
        runs INT,
        doubles INT,
        triples INT,
        homeRuns INT,
        rbi INT,
        baseOnBalls INT,
        strikeOuts INT,
        leftOnBase INT,
        date DATE
    )
    """
    return create_table_sql

def write_boxscore_to_sql(csv_file_path, connection_string):
    """Write boxscore CSV data to SQL Server database"""
    
    # Check if CSV file exists
    if not os.path.exists(csv_file_path):
        print(f"CSV file not found: {csv_file_path}")
        return
    
    # Read CSV file
    df = pd.read_csv(csv_file_path)
    
    # Clean data - replace NaN with None for SQL compatibility
    df = df.where(pd.notnull(df), None)
    
    # Convert data types as needed
    numeric_cols = ['gamePk', 'player_id', 'batting_order', 'gamesPlayed', 'atBats', 
                   'hits', 'runs', 'doubles', 'triples', 'homeRuns', 'rbi', 
                   'baseOnBalls', 'strikeOuts', 'leftOnBase']
    
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    try:
        # Connect to SQL Server using Windows Authentication
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        
        # Create table if it doesn't exist (for SQL Server, use CREATE TABLE without IF NOT EXISTS)
        create_table_sql = """
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='boxscore_batting' AND xtype='U')
        CREATE TABLE dbo.boxscore_batting (
            id INT IDENTITY(1,1) PRIMARY KEY,
            gamePk INT,
            team NVARCHAR(100),
            team_type NVARCHAR(10),
            player_id INT,
            player_name NVARCHAR(100),
            batting_order INT,
            gamesPlayed INT,
            atBats INT,
            hits INT,
            runs INT,
            doubles INT,
            triples INT,
            homeRuns INT,
            rbi INT,
            baseOnBalls INT,
            strikeOuts INT,
            leftOnBase INT,
            date DATE
        )
        """
        cursor.execute(create_table_sql)
        conn.commit()
        
        # Prepare insert statement
        insert_sql = """
        INSERT INTO dbo.boxscore_batting (
            gamePk, team, team_type, player_id, player_name, batting_order,
            gamesPlayed, atBats, hits, runs, doubles, triples, homeRuns,
            rbi, baseOnBalls, strikeOuts, leftOnBase, date
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        # Insert data row by row
        for row in df.itertuples(index=False, name=None):
            try:
                cursor.execute(insert_sql, *row)
            except Exception as e:
                print(f"Error inserting row: {row}")
                print(f"Error: {e}")
                continue
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"Successfully loaded {len(df)} records to SQL Server")
        
    except Exception as e:
        print(f"Error connecting to SQL Server: {e}")

# Alternative method using SQLAlchemy (often more reliable)
def write_boxscore_to_sql_alchemy(csv_file_path, connection_string):
    """Write boxscore CSV data to SQL Server using SQLAlchemy"""
    
    # Check if CSV file exists
    if not os.path.exists(csv_file_path):
        print(f"CSV file not found: {csv_file_path}")
        return
    
    # Read CSV file
    df = pd.read_csv(csv_file_path)
    
    # Clean data
    df = df.where(pd.notnull(df), None)
    
    try:
        # Create SQLAlchemy engine
        engine = create_engine(f"mssql+pyodbc:///?odbc_connect={connection_string}")
        
        # Write DataFrame to SQL
        df.to_sql('boxscore_batting', engine, if_exists='append', index=False, schema='dbo')
        
        print(f"Successfully loaded {len(df)} records to SQL Server using SQLAlchemy")
        
    except Exception as e:
        print(f"Error using SQLAlchemy: {e}")

# Usage example
if __name__ == "__main__":
    # Connection string for Windows Authentication
    connection_string = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=DESKTOP-TJG2020;"
        "DATABASE=mlb;"
        "Trusted_Connection=yes;"
    )
    
    # Write combined boxscore data to SQL
    csv_file = 'data/csv/boxscores/mlb_boxscores_2025-07-06_to_2025-07-18.csv'
    write_boxscore_to_sql(csv_file, connection_string)
    
    # Or write individual daily files
    # date_range = ['2025-07-06', '2025-07-07', '2025-07-08']  # Add all your dates
    # for date_str in date_range:
    #     csv_file = f'data/csv/boxscores/mlb_boxscores_{date_str}.csv'
    #     write_boxscore_to_sql(csv_file, connection_string)