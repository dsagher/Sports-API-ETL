import pandas as pd
from typing import TypedDict
import tomllib

def transform_leagues(data):

    response = data['response']
    date_pulled = data['date_pulled']
    transformed_data = []

    for l in response:
        league = l['league']
        country = l['country']
        seasons = l['seasons'][0]
        coverage = l['seasons'][0]['coverage']

        transformed_data.append({
            'date_pulled': date_pulled,
            'league_id': league['id'],
            'league_name': league['name'],
            'league_type': league['type'],
            'league_logo': league['logo'],
            'country_name': country['name'],
            'country_code': country['code'],
            'country_flag': country['flag'],
            'season_year': seasons['year'],
            'season_start': seasons['start'],
            'season_end': seasons['end'],
            'season_current': seasons['current'],
            'season_events': coverage['fixtures']['events'],
            'season_lineups': coverage['fixtures']['lineups'],
            'season_statistics_fixtures': coverage['fixtures']['statistics_fixtures'],
            'season_statistics_players': coverage['fixtures']['statistics_players'],
            'season_standings': coverage['standings'],
            'season_players': coverage['players'],
            'season_top_scorers': coverage['top_scorers'],
            'season_top_assists': coverage['top_assists'],
            'season_top_cards': coverage['top_cards'],
            'season_injuries': coverage['injuries'],
            'season_predictions': coverage['predictions'],
        })


    leagues_df = pd.DataFrame(transformed_data)

    return leagues_df

def transform_players(data):

    year = data['parameters']['season']
    league = data['parameters']['league']
    date_pulled = data['date_pulled']

    transformed_data = []
    for p in data['response']:
        player = p['player']
        stats_team = p['statistics'][0]['team']
        stats_league = p['statistics'][0]['league']
        stats_games = p['statistics'][0]['games']
        stats_subs = p['statistics'][0]['substitutes']
        stats_shots = p['statistics'][0]['shots']
        stats_goals = p['statistics'][0]['goals']
        stats_passes = p['statistics'][0]['passes']
        stats_tackles = p['statistics'][0]['tackles']
        stats_duels = p['statistics'][0]['duels']
        stats_dribbles = p['statistics'][0]['dribbles']
        stats_fouls = p['statistics'][0]['fouls']
        stats_cards = p['statistics'][0]['cards']
        stats_penalty = p['statistics'][0]['penalty']

        transformed_data.append({
            'date_pulled': date_pulled,
            'league_id': league,
            'year': year,
            'player_id': player['id'],
            'player_name': player['name'],
            'player_age': player['age'],
            'player_nationality': player['nationality'],
            'player_photo': player['photo'],
            'player_birth_date': player['birth']['date'],
            'player_birth_place': player['birth']['place'],
            'player_birth_country': player['birth']['country'],
            'player_height': player['height'],
            'player_weight': player['weight'],
            'player_injured': player['injured'],
            'player_team': stats_team['id'],
            'player_team_name': stats_team['name'],
            'player_team_logo': stats_team['logo'],
            'player_league': stats_league['id'],
            'player_league_name': stats_league['name'],
            'player_league_country': stats_league['country'],
            'player_league_logo': stats_league['logo'],
            'player_league_flag': stats_league['flag'],
            'player_league_season': stats_league['season'],
            'player_games_played': stats_games['appearences'],
            'player_minutes_played': stats_games['minutes'],
            'player_lineups': stats_games['lineups'],
            'player_number': stats_games['number'],
            'player_position': stats_games['position'],
            'player_rating': stats_games['rating'],
            'player_captain': stats_games['captain'],
            'player_sub_in': stats_subs['in'],
            'player_sub_out': stats_subs['out'],
            'player_sub_on_bench': stats_subs['bench'],
            'player_shots_total': stats_shots['total'],
            'player_shots_on': stats_shots['on'],
            'player_goals_total': stats_goals['total'],
            'player_goals_conceded': stats_goals['conceded'],
            'player_goals_assists': stats_goals['assists'],
            'player_saves': stats_goals['saves'],
            'player_passes_total': stats_passes['total'],
            'player_passes_key': stats_passes['key'],
            'player_passes_accuracy': stats_passes['accuracy'],
            'player_tackles_total': stats_tackles['total'],
            'player_tackles_blocks': stats_tackles['blocks'],
            'player_tackles_interceptions': stats_tackles['interceptions'],
            'player_duels_total': stats_duels['total'],
            'player_duels_won': stats_duels['won'],
            'player_dribbles_attempts': stats_dribbles['attempts'],
            'player_dribbles_success': stats_dribbles['success'],
            'player_dribbles_past': stats_dribbles['past'],
            'player_fouls_committed': stats_fouls['committed'],
            'player_fouls_drawn': stats_fouls['drawn'],
            'player_cards_yellow': stats_cards['yellow'],
            'player_cards_yellow_red': stats_cards['yellowred'],
            'player_cards_red': stats_cards['red'],
            'player_penalties_won': stats_penalty['won'],
            'player_penalties_commited': stats_penalty['commited'],
            'player_penalties_scored': stats_penalty['scored'],
            'player_penalties_missed': stats_penalty['missed'],
            'player_penalties_saved': stats_penalty['saved']
        })

    players_df = pd.DataFrame(transformed_data)
    return players_df

def transform_teams(data):

    year = data['parameters']['season']
    league = data['parameters']['league']
    date_pulled = data['date_pulled']
    transformed_data = []

    for t in data['response']:
        team = t['team']
        venue = t['venue']
        transformed_data.append({
            'date_pulled': date_pulled,
            'league_id': league,
            'year': year,
            'team_id': team['id'],
            'team_name': team['name'],
            'team_logo': team['logo'],
            'team_code': team['code'],
            'team_country': team['country'],
            'team_founded': team['founded'],
            'team_national': team['national'],
            'team_venue_id': venue['id'],
            'team_venue_name': venue['name'],
            'team_venue_address': venue['address'],
            'team_venue_city': venue['city'],
            'team_venue_surface': venue['surface'],
            'team_venue_image': venue['image'],
        })

    teams_df = pd.DataFrame(transformed_data)

    return teams_df