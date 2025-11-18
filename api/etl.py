import extract
import transform
from load import load_data

def etl(league_id, season_year):
    leagues = extract.get_leagues()
    leagues_df = transform.transform_leagues(leagues)
    players = extract.get_players_by_league_season(league_id, season_year)
    players_df = transform.transform_players(players)
    teams = extract.get_teams_by_league_season(league_id, season_year)
    teams_df = transform.transform_teams(teams)

    load_data(leagues_df, players_df, teams_df)

if __name__ == "__main__":
    etl(61, 2021)