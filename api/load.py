import sqlite3
import tomllib
import pandas as pd

def load_data(leagues_df, players_df, teams_df):
    conn = sqlite3.connect('football.db')
    leagues_df.to_sql('leagues', conn, if_exists='append', index=False)
    players_df.to_sql('players', conn, if_exists='append', index=False)
    teams_df.to_sql('teams', conn, if_exists='append', index=False)
    conn.close()

    print("Data loaded successfully")

def load_data_2(df:pd.DataFrame, df_name: str):
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
    sql = f"INSERT INTO leagues ({col_str}) VALUES ({placeholders});"

    cursor.executemany(sql, rows)
    conn.commit()
    conn.close()
    print("Leagues loaded successfully from DataFrame")

if __name__ == "__main__":
    leagues = pd.read_csv('processed_data/leagues.csv')
    load_data_2(leagues, "leagues")
    # pass