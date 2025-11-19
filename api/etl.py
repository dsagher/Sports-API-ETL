import logging
import extract
import transform
from load import load_data, write_to_csv

logger = logging.getLogger(__name__)


def etl(league_id: int, season_year: int) -> None:
    """
    Execute ETL pipeline for a given league and season.
    
    Args:
        league_id: The ID of the league to process
        season_year: The season year to process (must be between 2021 and 2023)
    
    Raises:
        ValueError: If season_year is out of valid range
        Exception: If any step of the ETL process fails
    """
    logger.info(f"Starting ETL process for league_id={league_id}, season={season_year}")
    
    try:
        # Extract
        logger.info("Extracting league data...")
        leagues = extract.get_leagues(league_id)
        logger.info("Extracting player data...")
        players = extract.get_players_by_league_season(league_id, season_year)
        logger.info("Extracting team data...")
        teams = extract.get_teams_by_league_season(league_id, season_year)
        
        # Transform
        logger.info("Transforming league data...")
        leagues_df = transform.transform_leagues(leagues)
        logger.info("Transforming player data...")
        players_df = transform.transform_players(players)
        logger.info("Transforming team data...")
        teams_df = transform.transform_teams(teams)
        
        # Load
        logger.info("Loading data into database...")
        load_data(leagues_df, "leagues")
        load_data(players_df, "players")
        load_data(teams_df, "teams")
        
        logger.info("Writing data to CSV files...")
        write_to_csv(leagues_df, "leagues", league_id, season_year)
        write_to_csv(players_df, "players", league_id, season_year)
        write_to_csv(teams_df, "teams", league_id, season_year)
        
        logger.info(f"ETL process completed successfully for league_id={league_id}, season={season_year}")
    except Exception as e:
        logger.error(f"ETL process failed for league_id={league_id}, season={season_year}: {e}")
        raise

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    etl(39, 2021)
    # etl(39, 2022)
    # etl(39, 2023)
    # etl(40, 2021)
    # etl(40, 2022)
    # etl(40, 2023)
    pass