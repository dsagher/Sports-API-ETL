from dotenv import load_dotenv
import os
import logging
import requests
import datetime
from typing import Dict, Any

# Configure logging
logger = logging.getLogger(__name__)

load_dotenv()
api_key = os.getenv('API_KEY')

if not api_key:
    raise ValueError("API key not found. Please set API_KEY in your .env file")

# API info
BASE_URL = "https://v3.football.api-sports.io"
HEADERS = {
    "x-apisports-key": api_key
}



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
    url = f"{BASE_URL}/players?season={season_year}&league={league_id}"

    try:
        logger.info(f"Fetching players for league_id={league_id}, season={season_year}")
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if 'response' not in data:
            raise ValueError("API response missing 'response' key")
        
        data['date_pulled'] = date_pulled
        logger.info(f"Successfully fetched {len(data.get('response', []))} players")
        return data
    except requests.RequestException as e:
        logger.error(f"Error fetching players for league_id={league_id}, season={season_year}: {e}")
        raise

def get_teams_by_league_season(league_id: int, season_year: int) -> Dict[str, Any]:
    """
    Get teams by league and season from the API.

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
