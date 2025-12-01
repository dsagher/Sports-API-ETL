import os
import logging
import requests
import datetime
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

QUERY_COUNT_FILE_PATH = "query_count.txt"
PAGE_FILE_PATH = "last_page.txt"
DATE_FMT = "%m/%d/%Y"
DAILY_LIMIT = 100
PAGE_LIMIT = 3
def get_last_page():
    if not os.path.exists(PAGE_FILE_PATH):
        return 1
    with open(PAGE_FILE_PATH, "r") as f:
        page = f.read()
        return int(page)

def write_page(page):
    with open(PAGE_FILE_PATH, "w") as f:
        if page == PAGE_LIMIT:
            f.write(str(1))
        else:
            f.write(page)
    logger.info(f"Wrote last page number ({page}) to last_page.txt")


def get_query_count():
    """
    Returns (count: int, date_str: str) where date_str is in DATE_FMT.
    If file doesn't exist, initializes it with count 1 for today.
    """
    if not os.path.exists(QUERY_COUNT_FILE_PATH):
        today_str = datetime.datetime.now().strftime(DATE_FMT)
        with open(QUERY_COUNT_FILE_PATH, "x") as f:
            f.write(f"1, {today_str}")
        return 1, today_str

    with open(QUERY_COUNT_FILE_PATH, "r") as f:
        content = f.read().strip()

    if not content:
        today_str = datetime.datetime.now().strftime(DATE_FMT)
        with open(QUERY_COUNT_FILE_PATH, "w") as f:
            f.write(f"1, {today_str}")
        return 1, today_str

    count_str, date_str = content.split(", ")
    return int(count_str), date_str

    
def write_query_count():
    """
    Increments the query count for the current day.
    Resets to 1 if the stored date is not today.
    Raises ValueError if DAILY_LIMIT would be exceeded.
    """
    count, stored_date_str = get_query_count()

    today = datetime.datetime.now().date()
    stored_date = datetime.datetime.strptime(stored_date_str, DATE_FMT).date()

    if stored_date != today:
        new_count = 1
        new_date_str = today.strftime(DATE_FMT)
    else:
        if count >= DAILY_LIMIT:
            raise ValueError("API Rate Limit Reached")
        new_count = count + 1
        new_date_str = stored_date_str 

    with open(QUERY_COUNT_FILE_PATH, "w") as f:
        f.write(f"{new_count}, {new_date_str}")


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

        write_query_count()

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
    try:
        while True:
            url = f"{BASE_URL}/players?season={season_year}&league={league_id}&page={page}"
            logger.info(f"Fetching players page {page} for league_id={league_id}, season={season_year}")
            
            response = requests.get(url, headers=HEADERS, timeout=30)

            write_query_count()
            response.raise_for_status()
            data = response.json()

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
        write_query_count()
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
