from dotenv import load_dotenv
import os
import requests
import datetime

load_dotenv()
api_key = os.getenv('API_KEY')

if not api_key:
    raise ValueError("API key not found")

# API info
BASE_URL = "https://v3.football.api-sports.io"
HEADERS = {
    "x-apisports-key": api_key
}



def get_leagues(league_id: int) -> dict:
    """
    Get all leagues from the API

    Returns:
        data: dict
    """
    DATE_PULLED = datetime.datetime.now().strftime('%m/%d/%Y')

    url = f"{BASE_URL}/leagues?id={league_id}"

    response = requests.get(url, headers=HEADERS)

    response.raise_for_status()

    data = response.json()

    data['date_pulled'] = DATE_PULLED

    return data

def get_players_by_league_season(league_id: int, season_year: int) -> dict:
    """
    Get players by league and season from the API

    Returns:
        data: dict
    """
    DATE_PULLED = datetime.datetime.now().strftime('%m/%d/%Y')

    url = f"{BASE_URL}/players?season={season_year}&league={league_id}"

    if season_year < 2021 or season_year > 2023:
        raise ValueError("Season year must be between 2021 and 2023")

    response = requests.get(url, headers=HEADERS)

    response.raise_for_status()

    data = response.json()

    data['date_pulled'] = DATE_PULLED

    return data

def get_teams_by_league_season(league_id: int, season_year: int) -> dict:
    """
    Get teams by league and season from the API

    Returns:
        data: dict
    """
    DATE_PULLED = datetime.datetime.now().strftime('%m/%d/%Y')

    url = f"{BASE_URL}/teams?league={league_id}&season={season_year}"

    if season_year < 2021 or season_year > 2023:
        raise ValueError("Season year must be between 2021 and 2023")

    response = requests.get(url, headers=HEADERS)

    response.raise_for_status()

    data = response.json()

    data['date_pulled'] = DATE_PULLED

    return data
