import sqlite3

def load_data(leagues_df, players_df, teams_df):
    conn = sqlite3.connect('football.db')
    leagues_df.to_sql('leagues', conn, if_exists='append', index=False)
    players_df.to_sql('players', conn, if_exists='append', index=False)
    teams_df.to_sql('teams', conn, if_exists='append', index=False)
    conn.close()

    print("Data loaded successfully")