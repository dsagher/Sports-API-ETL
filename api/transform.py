import pandas as pd
import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def transform_leagues(data: Dict[str, Any]) -> pd.DataFrame:
    """
    Transform league data from API response into a DataFrame.
    
    Args:
        data: Dictionary containing API response with 'response' and 'date_pulled' keys
    
    Returns:
        DataFrame with transformed league data
    
    Raises:
        KeyError: If required keys are missing from the data structure
        IndexError: If seasons list is empty
    """
    if 'response' not in data:
        raise KeyError("Data missing required 'response' key")
    if 'date_pulled' not in data:
        raise KeyError("Data missing required 'date_pulled' key")
    if data['errors']:
        error_msg = f"API returned errors: {data.get('errors')}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    response = data['response']
    date_pulled = data['date_pulled']
    transformed_data: List[Dict[str, Any]] = []

    for idx, l in enumerate(response):
        try:
            if 'league' not in l:
                logger.warning(f"Skipping league entry {idx}: missing 'league' key")
                continue
            if 'country' not in l:
                logger.warning(f"Skipping league entry {idx}: missing 'country' key")
                continue
            if 'seasons' not in l or not l['seasons']:
                logger.warning(f"Skipping league entry {idx}: missing or empty 'seasons'")
                continue
            
            league = l['league']
            country = l['country']
            seasons = l['seasons'][0]
            
            if 'coverage' not in seasons:
                logger.warning(f"Skipping league entry {idx}: missing 'coverage' in seasons")
                continue
            
            coverage = seasons['coverage']

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
            'season_predictions': coverage.get('predictions', False),
            })
        except (KeyError, IndexError) as e:
            logger.warning(f"Error processing league entry {idx}: {e}")
            continue

    if not transformed_data:
        logger.warning("No valid league data to transform")
        return pd.DataFrame()

    leagues_df = pd.DataFrame(transformed_data)
    logger.info(f"Successfully transformed {len(leagues_df)} leagues")
    return leagues_df


def transform_players(data: Dict[str, Any]) -> pd.DataFrame:
    """
    Transform player data from API response into a DataFrame.
    
    Args:
        data: Dictionary containing API response with 'response', 'parameters', and 'date_pulled' keys
    
    Returns:
        DataFrame with transformed player data
    
    Raises:
        KeyError: If required keys are missing from the data structure
        IndexError: If statistics list is empty
    """
    try:
        year = data['parameters']['season']
        league = data['parameters']['league']
    except KeyError as e:
        raise KeyError(f"Parameters missing required key: {e}")
    
    date_pulled = data['date_pulled']
    transformed_data: List[Dict[str, Any]] = []
    
    for idx, p in enumerate(data['response']):
        try:
            if 'player' not in p:
                logger.warning(f"Skipping player entry {idx}: missing 'player' key")
                continue
            if 'statistics' not in p or not p['statistics']:
                logger.warning(f"Skipping player entry {idx}: missing or empty 'statistics'")
                continue
            
            player = p['player']
            stats = p['statistics'][0]
            
            stats_team = stats.get('team', {})
            stats_league = stats.get('league', {})
            stats_games = stats.get('games', {})
            stats_subs = stats.get('substitutes', {})
            stats_shots = stats.get('shots', {})
            stats_goals = stats.get('goals', {})
            stats_passes = stats.get('passes', {})
            stats_tackles = stats.get('tackles', {})
            stats_duels = stats.get('duels', {})
            stats_dribbles = stats.get('dribbles', {})
            stats_fouls = stats.get('fouls', {})
            stats_cards = stats.get('cards', {})
            stats_penalty = stats.get('penalty', {})
            
            birth = player.get('birth', {})

            transformed_data.append({
                'date_pulled': date_pulled,
                'league_id': league,
                'year': year,
                'player_id': player.get('id'),
                'player_name': player.get('name'),
                'player_age': player.get('age'),
                'player_nationality': player.get('nationality'),
                'player_photo': player.get('photo'),
                'player_birth_date': birth.get('date'),
                'player_birth_place': birth.get('place'),
                'player_birth_country': birth.get('country'),
                'player_height': player.get('height'),
                'player_weight': player.get('weight'),
                'player_injured': player.get('injured', False),
                'player_team': stats_team.get('id'),
                'player_team_name': stats_team.get('name'),
                'player_team_logo': stats_team.get('logo'),
                'player_league': stats_league.get('id'),
                'player_league_name': stats_league.get('name'),
                'player_league_country': stats_league.get('country'),
                'player_league_logo': stats_league.get('logo'),
                'player_league_flag': stats_league.get('flag'),
                'player_league_season': stats_league.get('season'),
                'player_games_played': stats_games.get('appearences'),
                'player_minutes_played': stats_games.get('minutes'),
                'player_lineups': stats_games.get('lineups'),
                'player_number': stats_games.get('number'),
                'player_position': stats_games.get('position'),
                'player_rating': stats_games.get('rating'),
                'player_captain': stats_games.get('captain', False),
                'player_sub_in': stats_subs.get('in'),
                'player_sub_out': stats_subs.get('out'),
                'player_sub_on_bench': stats_subs.get('bench'),
                'player_shots_total': stats_shots.get('total'),
                'player_shots_on': stats_shots.get('on'),
                'player_goals_total': stats_goals.get('total'),
                'player_goals_conceded': stats_goals.get('conceded'),
                'player_goals_assists': stats_goals.get('assists'),
                'player_saves': stats_goals.get('saves'),
                'player_passes_total': stats_passes.get('total'),
                'player_passes_key': stats_passes.get('key'),
                'player_passes_accuracy': stats_passes.get('accuracy'),
                'player_tackles_total': stats_tackles.get('total'),
                'player_tackles_blocks': stats_tackles.get('blocks'),
                'player_tackles_interceptions': stats_tackles.get('interceptions'),
                'player_duels_total': stats_duels.get('total'),
                'player_duels_won': stats_duels.get('won'),
                'player_dribbles_attempts': stats_dribbles.get('attempts'),
                'player_dribbles_success': stats_dribbles.get('success'),
                'player_dribbles_past': stats_dribbles.get('past'),
                'player_fouls_committed': stats_fouls.get('committed'),
                'player_fouls_drawn': stats_fouls.get('drawn'),
                'player_cards_yellow': stats_cards.get('yellow'),
                'player_cards_yellow_red': stats_cards.get('yellowred'),
                'player_cards_red': stats_cards.get('red'),
                'player_penalties_won': stats_penalty.get('won'),
                'player_penalties_commited': stats_penalty.get('commited'),
                'player_penalties_scored': stats_penalty.get('scored'),
                'player_penalties_missed': stats_penalty.get('missed'),
                'player_penalties_saved': stats_penalty.get('saved')
            })
        except (KeyError, IndexError) as e:
            logger.warning(f"Error processing player entry {idx}: {e}")
            continue

    if not transformed_data:
        logger.warning("No valid player data to transform")
        return pd.DataFrame()

    players_df = pd.DataFrame(transformed_data)
    logger.info(f"Successfully transformed {len(players_df)} players")
    return players_df

def transform_teams(data: Dict[str, Any]) -> pd.DataFrame:
    """
    Transform team data from API response into a DataFrame.
    
    Args:
        data: Dictionary containing API response with 'response', 'parameters', and 'date_pulled' keys
    
    Returns:
        DataFrame with transformed team data
    
    Raises:
        KeyError: If required keys are missing from the data structure
    """
    if 'response' not in data:
        raise KeyError("Data missing required 'response' key")
    if 'parameters' not in data:
        raise KeyError("Data missing required 'parameters' key")
    if 'date_pulled' not in data:
        raise KeyError("Data missing required 'date_pulled' key")
    if data['errors']:
        error_msg = f"API returned errors: {data.get('errors')}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    try:
        year = data['parameters']['season']
        league = data['parameters']['league']
    except KeyError as e:
        raise KeyError(f"Parameters missing required key: {e}")
    
    date_pulled = data['date_pulled']
    transformed_data: List[Dict[str, Any]] = []

    for idx, t in enumerate(data['response']):
        try:
            if 'team' not in t:
                logger.warning(f"Skipping team entry {idx}: missing 'team' key")
                continue
            if 'venue' not in t:
                logger.warning(f"Skipping team entry {idx}: missing 'venue' key")
                continue
            
            team = t['team']
            venue = t['venue']
            transformed_data.append({
                'date_pulled': date_pulled,
                'league_id': league,
                'year': year,
                'team_id': team.get('id'),
                'team_name': team.get('name'),
                'team_logo': team.get('logo'),
                'team_code': team.get('code'),
                'team_country': team.get('country'),
                'team_founded': team.get('founded'),
                'team_national': team.get('national', False),
                'team_venue_id': venue.get('id'),
                'team_venue_name': venue.get('name'),
                'team_venue_address': venue.get('address'),
                'team_venue_city': venue.get('city'),
                'team_venue_surface': venue.get('surface'),
                'team_venue_image': venue.get('image'),
            })
        except (KeyError, TypeError) as e:
            logger.warning(f"Error processing team entry {idx}: {e}")
            continue

    if not transformed_data:
        logger.warning("No valid team data to transform")
        return pd.DataFrame()

    teams_df = pd.DataFrame(transformed_data)
    logger.info(f"Successfully transformed {len(teams_df)} teams")
    return teams_df