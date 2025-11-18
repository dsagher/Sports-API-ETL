import pandas as pd
from typing import TypedDict
import tomllib

def transform_leagues(data):

    response = data['response']

    england_leagues = [i for i in response if i['country']['name'] == 'England']
    transformed_data = []

    for league in england_leagues:
        league = league['league']
        country = league['country']
        seasons = league['seasons'][0]
        coverage = league['seasons'][0]['coverage']
        fixtures = league['seaon']


        transformed_data.append({
            'league_id': league['league']['id'],
            'league_name': league['league']['name'],
            'league_type': league['league']['type'],
            'league_logo': league['league']['logo'],
            'country_name': league['country']['name'],
            'country_code': league['country']['code'],
            'country_flag': league['country']['flag'],
            'season_year': league['seasons'][0]['year'],
            'season_start': league['seasons'][0]['start'],
            'season_end': league['seasons'][0]['end'],
            'season_current': league['seasons'][0]['current'],
            'season_events': league['seasons'][0]['coverage']['fixtures']['events'],
            'season_lineups': league['seasons'][0]['coverage']['fixtures']['lineups'],
            'season_statistics_fixtures': league['seasons'][0]['coverage']['fixtures']['statistics_fixtures'],
            'season_statistics_players': league['seasons'][0]['coverage']['fixtures']['statistics_players'],
            'season_standings': league['seasons'][0]['coverage']['standings'],
            'season_players': league['seasons'][0]['coverage']['players'],
            'season_top_scorers': league['seasons'][0]['coverage']['top_scorers'],
            'season_top_assists': league['seasons'][0]['coverage']['top_assists'],
            'season_top_cards': league['seasons'][0]['coverage']['top_cards'],
            'season_injuries': league['seasons'][0]['coverage']['injuries'],
            'season_predictions': league['seasons'][0]['coverage']['predictions'],
        })


    leagues_df = pd.DataFrame(transformed_data)

    return leagues_df

def transform_players(data):

    year = data['parameters']['season']
    league = data['parameters']['league']

    transformed_data = []
    for player in data['response']:
        transformed_data.append({
            'league_id': league,
            'year': year,
            'player_id': player['player']['id'],
            'player_name': player['player']['name'],
            'player_age': player['player']['age'],
            'player_nationality': player['player']['nationality'],
            'player_photo': player['player']['photo'],
            'player_birth_date': player['player']['birth']['date'],
            'player_birth_place': player['player']['birth']['place'],
            'player_birth_country': player['player']['birth']['country'],
            'player_height': player['player']['height'],
            'player_weight': player['player']['weight'],
            'player_injured': player['player']['injured'],
            'player_team': player['statistics'][0]['team']['id'],
            'player_team_name': player['statistics'][0]['team']['name'],
            'player_team_logo': player['statistics'][0]['team']['logo'],
            'player_league': player['statistics'][0]['league']['id'],
            'player_league_name': player['statistics'][0]['league']['name'],
            'player_league_country': player['statistics'][0]['league']['country'],
            'player_league_logo': player['statistics'][0]['league']['logo'],
            'player_league_flag': player['statistics'][0]['league']['flag'],
            'player_league_season': player['statistics'][0]['league']['season'],
            'player_games_played': player['statistics'][0]['games']['appearences'],
            'player_minutes_played': player['statistics'][0]['games']['minutes'],
            'player_lineups': player['statistics'][0]['games']['lineups'],
            'player_number': player['statistics'][0]['games']['number'],
            'player_position': player['statistics'][0]['games']['position'],
            'player_rating': player['statistics'][0]['games']['rating'],
            'player_captain': player['statistics'][0]['games']['captain'],
            'player_sub_in': player['statistics'][0]['substitutes']['in'],
            'player_sub_out': player['statistics'][0]['substitutes']['out'],
            'player_sub_on_bench': player['statistics'][0]['substitutes']['bench'],
            'player_shots_total': player['statistics'][0]['shots']['total'],
            'player_shots_on': player['statistics'][0]['shots']['on'],
            'player_goals_total': player['statistics'][0]['goals']['total'],
            'player_goals_conceded': player['statistics'][0]['goals']['conceded'],
            'player_goals_assists': player['statistics'][0]['goals']['assists'],
            'player_saves': player['statistics'][0]['goals']['saves'],
            'player_passes_total': player['statistics'][0]['passes']['total'],
            'player_passes_key': player['statistics'][0]['passes']['key'],
            'player_passes_accuracy': player['statistics'][0]['passes']['accuracy'],
            'player_tackles_total': player['statistics'][0]['tackles']['total'],
            'player_tackles_blocks': player['statistics'][0]['tackles']['blocks'],
            'player_tackles_interceptions': player['statistics'][0]['tackles']['interceptions'],
            'player_duels_total': player['statistics'][0]['duels']['total'],
            'player_duels_won': player['statistics'][0]['duels']['won'],
            'player_dribbles_attempts': player['statistics'][0]['dribbles']['attempts'],
            'player_dribbles_success': player['statistics'][0]['dribbles']['success'],
            'player_dribbles_past': player['statistics'][0]['dribbles']['past'],
            'player_fouls_committed': player['statistics'][0]['fouls']['committed'],
            'player_fouls_drawn': player['statistics'][0]['fouls']['drawn'],
            'player_cards_yellow': player['statistics'][0]['cards']['yellow'],
            'player_cards_yellow_red': player['statistics'][0]['cards']['yellowred'],
            'player_cards_red': player['statistics'][0]['cards']['red'],
            'player_penalties_won': player['statistics'][0]['penalty']['won'],
            'player_penalties_commited': player['statistics'][0]['penalty']['commited'],
            'player_penalties_scored': player['statistics'][0]['penalty']['scored'],
            'player_penalties_missed': player['statistics'][0]['penalty']['missed'],
            'player_penalties_saved': player['statistics'][0]['penalty']['saved'],
        })

    players_df = pd.DataFrame(transformed_data)
    return players_df

def transform_teams(data):

    year = data['parameters']['season']
    league = data['parameters']['league']

    transformed_data = []

    for team in data['response']:
        transformed_data.append({
            'league_id': league,
            'year': year,
            'team_id': team['team']['id'],
            'team_name': team['team']['name'],
            'team_logo': team['team']['logo'],
            'team_code': team['team']['code'],
            'team_country': team['team']['country'],
            'team_founded': team['team']['founded'],
            'team_national': team['team']['national'],
            'team_venue_id': team['venue']['id'],
            'team_venue_name': team['venue']['name'],
            'team_venue_address': team['venue']['address'],
            'team_venue_city': team['venue']['city'],
            'team_venue_surface': team['venue']['surface'],
            'team_venue_image': team['venue']['image'],
        })

    teams_df = pd.DataFrame(transformed_data)

    return teams_df