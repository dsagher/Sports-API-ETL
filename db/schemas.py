import sqlite3

def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leagues (
            league_id INTEGER,
            league_name TEXT,
            league_type TEXT,
            league_logo TEXT,
            country_name TEXT,
            country_code TEXT,
            country_flag TEXT,
            season_year INTEGER,
            season_start TEXT,
            season_end TEXT,
            season_current BOOLEAN,
            season_events BOOLEAN,
            season_lineups BOOLEAN,
            season_statistics_fixtures BOOLEAN,
            season_statistics_players BOOLEAN,
            season_standings BOOLEAN,
            season_players BOOLEAN,
            season_top_scorers BOOLEAN,
            season_top_assists BOOLEAN,
            season_top_cards BOOLEAN,
            season_injuries BOOLEAN,
            season_predictions BOOLEAN,
            date_pulled TEXT,
            PRIMARY KEY (league_id, season_year, date_pulled)
        )""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            league_id INTEGER,
            year INTEGER,  
            player_id INTEGER,
            player_name TEXT,
            player_age INTEGER,
            player_nationality TEXT,
            player_photo TEXT,
            player_birth_date TEXT,
            player_birth_place TEXT,
            player_birth_country TEXT,
            player_height TEXT,
            player_weight TEXT,
            player_injured BOOLEAN,
            player_team INTEGER,
            player_team_name TEXT,
            player_team_logo TEXT,
            player_league INTEGER,
            player_league_name TEXT,
            player_league_country TEXT,
            player_league_logo TEXT,
            player_league_flag TEXT,
            player_league_season INTEGER,
            player_games_played INTEGER,
            player_minutes_played INTEGER,
            player_lineups INTEGER,
            player_number INTEGER,
            player_position TEXT,
            player_rating REAL,
            player_captain BOOLEAN,
            player_sub_in INTEGER,
            player_sub_out INTEGER,
            player_sub_on_bench INTEGER,
            player_shots_total INTEGER,
            player_shots_on INTEGER,
            player_goals_total INTEGER,
            player_goals_conceded INTEGER,
            player_goals_assists INTEGER,
            player_saves INTEGER,
            player_passes_total INTEGER,
            player_passes_key INTEGER,
            player_passes_accuracy TEXT,
            player_tackles_total INTEGER,
            player_tackles_blocks INTEGER,
            player_tackles_interceptions INTEGER,
            player_duels_total INTEGER,
            player_duels_won INTEGER,
            player_dribbles_attempts INTEGER,
            player_dribbles_success INTEGER,
            player_dribbles_past INTEGER,
            player_fouls_committed INTEGER,
            player_fouls_drawn INTEGER,
            player_cards_yellow INTEGER,
            player_cards_yellow_red INTEGER,
            player_cards_red INTEGER,
            player_penalties_won INTEGER,
            player_penalties_commited INTEGER,
            player_penalties_scored INTEGER,
            player_penalties_missed INTEGER,
            player_penalties_saved INTEGER,
            date_pulled TEXT,
            PRIMARY KEY (league_id, year, player_id, date_pulled)
        )""")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teams (
        league_id INTEGER,
        year INTEGER,
        team_id INTEGER,
        team_name TEXT,
        team_logo TEXT,
        team_code TEXT,
        team_country TEXT,
        team_founded INTEGER,
        team_national BOOLEAN,
        team_venue_id INTEGER,
        team_venue_name TEXT,
        team_venue_address TEXT,
        team_venue_city TEXT,
        team_venue_surface TEXT,
        team_venue_image TEXT,
        date_pulled TEXT,
        PRIMARY KEY (league_id, year, team_id, date_pulled)
        )""")
    conn.commit()
    conn.close()
    print("Tables created successfully")
    return True


def drop_tables(conn):
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS leagues")
    cursor.execute("DROP TABLE IF EXISTS players")
    cursor.execute("DROP TABLE IF EXISTS teams")
    conn.commit()
    conn.close()
    print("Tables dropped successfully")

if __name__ == "__main__":
    conn = sqlite3.connect('football.db')
    drop_tables(conn)
    conn = sqlite3.connect('football.db')
    create_tables(conn)
    conn.close()