import os
import logging
import requests
import datetime
import json
from typing import Dict, Any

# Configure logging
logger = logging.getLogger(__name__)

api_key = os.getenv('API_KEY')
if not api_key:
    raise ValueError("API key not found. Please set API_KEY in your .env file")

# API info
BASE_URL = "https://v3.football.api-sports.io"
HEADERS = {
    "x-apisports-key": api_key
}


def get_last_page():
    if not os.path.exists("last_page.txt"):
        return 1
    with open("last_page.txt", "r") as f:
        return int(f.read())

def write_page(page):
    with open("last_page.txt", "w") as f:
        f.write(str(page))
    logger.info(f"Wrote last page number ({page}) to last_page.txt")

def get_leagues(league_id: int) -> Dict[str, Any]:
    """
    Get all leagues from the API.

    Args:
        league_id: The ID of the league to retrieve

    Returns:
        Dictionary containing league data with 'date_pulled' field added

    Raises:
        requests.RequestException: If the API request fails
        ValueError: If the response doesn't contain expected data
    """
    date_pulled = datetime.datetime.now().strftime('%m/%d/%Y')
    url = f"{BASE_URL}/leagues?id={league_id}"

    try:
        logger.info(f"Fetching leagues for league_id={league_id}")
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if 'response' not in data:
            raise ValueError("API response missing 'response' key")
        
        data['date_pulled'] = date_pulled
        logger.info(f"Successfully fetched {len(data.get('response', []))} leagues")
        return data
    except requests.RequestException as e:
        logger.error(f"Error fetching leagues for league_id={league_id}: {e}")
        raise

def get_players_by_league_season(league_id: int, season_year: int) -> Dict[str, Any]:
    """
    Get players by league and season from the API.
    Handles pagination to fetch all players.

    Args:
        league_id: The ID of the league
        season_year: The season year (must be between 2021 and 2023)

    Returns:
        Dictionary containing player data with 'date_pulled' field added

    Raises:
        ValueError: If season_year is out of valid range or response is invalid
        requests.RequestException: If the API request fails
    """
    if season_year < 2021 or season_year > 2023:
        raise ValueError("Season year must be between 2021 and 2023")

    date_pulled = datetime.datetime.now().strftime('%m/%d/%Y')
    all_players = []
    page = get_last_page()
    PAGE_LIMIT = 3
    try:
        while True:
            url = f"{BASE_URL}/players?season={season_year}&league={league_id}&page={page}"
            logger.info(f"Fetching players page {page} for league_id={league_id}, season={season_year}")
            
            response = requests.get(url, headers=HEADERS, timeout=30)
            response.raise_for_status()
            data = response.json()
            print("DATA", data)
            if 'response' not in data:
                raise ValueError("API response missing 'response' key")
            if 'errors' in data and data['errors']:
                error_msg = f"API returned errors: {data.get('errors')}"
                logger.error(error_msg)
                raise ValueError(error_msg)
            if 'parameters' not in data:
                raise ValueError("Data missing required 'parameters' key")
            
            players = data.get('response', [])
            if not players:
                break
            
            all_players.extend(players)
            
            # Check if there are more pages
            paging = data.get('paging', {})
            current_page = paging.get('current', page)
            total_pages = paging.get('total', 1)
            
            logger.info(f"Fetched {len(players)} players from page {current_page}/{total_pages}")
            
            if current_page >= total_pages:
                break
            if page >= PAGE_LIMIT:
                break
            page += 1
        

        write_page(page)
        result = {
            'response': all_players,
            'parameters': data.get('parameters', {}),
            'date_pulled': date_pulled
        }
        
        logger.info(f"Successfully fetched {len(all_players)} total players")
        return result
    except requests.RequestException as e:
        logger.error(f"Error fetching players for league_id={league_id}, season={season_year}: {e}")
        raise

def get_teams_by_league_season(league_id: int, season_year: int) -> Dict[str, Any]:
    """
    Get teams by league and season from the API.
    Handles pagination to fetch all teams.

    Args:
        league_id: The ID of the league
        season_year: The season year (must be between 2021 and 2023)

    Returns:
        Dictionary containing team data with 'date_pulled' field added

    Raises:
        ValueError: If season_year is out of valid range or response is invalid
        requests.RequestException: If the API request fails
    """
    if season_year < 2021 or season_year > 2023:
        raise ValueError("Season year must be between 2021 and 2023")

    date_pulled = datetime.datetime.now().strftime('%m/%d/%Y')
    url = f"{BASE_URL}/teams?league={league_id}&season={season_year}"

    try:
        logger.info(f"Fetching teams for league_id={league_id}, season={season_year}")
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if 'response' not in data:
            raise ValueError("API response missing 'response' key")
        
        data['date_pulled'] = date_pulled
        logger.info(f"Successfully fetched {len(data.get('response', []))} teams")
        return data
    except requests.RequestException as e:
        logger.error(f"Error fetching teams for league_id={league_id}, season={season_year}: {e}")
        raise
