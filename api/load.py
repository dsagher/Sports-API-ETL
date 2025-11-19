import sqlite3
import tomllib
import pandas as pd
from typing import Literal


def load_data(df:pd.DataFrame, df_name: Literal["leagues","players","teams"]):

    conn = sqlite3.connect('football.db')

    cursor = conn.cursor()
    
    with open('./config.toml', 'rb') as f:
        config = tomllib.load(f)
        if df_name == "leagues":
            columns = config['columns']['league']
            values = ["?" for _ in columns]
        elif df_name == "players":
            columns = config['columns']['players']
            values = ["?" for _ in columns]
        elif df_name == "teams":
            columns = config['columns']['teams']
            values = ["?" for _ in columns]

    ordered = df[columns]

    rows = list(ordered.itertuples(index=False, name=None))

    col_str = ", ".join(columns)        
    placeholders = ", ".join(values)   
    sql = f"INSERT INTO {df_name} ({col_str}) VALUES ({placeholders});"

    try:
        cursor.executemany(sql, rows)
    except sqlite3.IntegrityError as e:
        print(f"Error executing SQL statement: {e}")
        conn.close()
        return
    
    conn.commit()
    conn.close()
    print("Leagues loaded successfully from DataFrame")

def write_to_csv(df: pd.DataFrame, df_name: str, league_id: int, season_year: int) -> None:
    df.to_csv(f"processed_data/{df_name}_{league_id}_{season_year}.csv")
    print("Successfully wrote to CSV.")

if __name__ == "__main__":
    leagues = pd.read_csv('processed_data/leagues.csv')
    load_data(leagues, "leagues")
    # pass