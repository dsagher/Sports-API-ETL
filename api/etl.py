import extract
import transform
from load import load_data, write_to_csv


def etl(league_id, season_year):
    leagues = extract.get_leagues(league_id)
    leagues_df = transform.transform_leagues(leagues)
    players = extract.get_players_by_league_season(league_id, season_year)
    players_df = transform.transform_players(players)
    teams = extract.get_teams_by_league_season(league_id, season_year)
    teams_df = transform.transform_teams(teams)

    load_data(leagues_df, "leagues")
    load_data(players_df, "players")
    load_data(teams_df, "teams")

    write_to_csv(leagues_df, "leagues", league_id, season_year)
    write_to_csv(players_df, "players", league_id, season_year)
    write_to_csv(teams_df, "teams", league_id, season_year)

if __name__ == "__main__":
    # etl(39, 2021)
    # etl(39, 2022)
    # etl(39, 2023)
    # etl(40, 2021)
    # etl(40, 2022)
    # etl(40, 2023)
    pass