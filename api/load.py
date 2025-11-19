import sqlite3
import tomllib
import logging
import pandas as pd
from typing import Any, Literal
from pathlib import Path

# Configure logging
logger = logging.getLogger(__name__)

# Whitelist of allowed table names to prevent SQL injection
ALLOWED_TABLES = {"leagues", "players", "teams"}


def _load_config() -> dict:
    """Load configuration from config.toml"""
    config_path = Path(__file__).parent.parent / "config.toml"
    with open(config_path, 'rb') as f:
        return tomllib.load(f)


def load_data(df: pd.DataFrame, df_name: Literal["leagues", "players", "teams"]) -> None:
    """
    Load DataFrame into SQLite database.
    
    Args:
        df: DataFrame to load
        df_name: Name of the table to insert into (must be in ALLOWED_TABLES)
    
    Raises:
        ValueError: If df_name is not in allowed tables
        KeyError: If required columns are missing from DataFrame
    """
    if df_name not in ALLOWED_TABLES:
        raise ValueError(f"Table name '{df_name}' is not allowed. Must be one of {ALLOWED_TABLES}")
    
    config = _load_config()
    db_path = config['database']['path']
    
    # Get columns from config
    column_mapping = {
        "leagues": config['columns']['league'],
        "players": config['columns']['players'],
        "teams": config['columns']['teams']
    }
    
    columns = column_mapping[df_name]
    values = ["?" for _ in columns]
    
    # Validate that DataFrame has required columns
    missing_columns = set[Any](columns) - set[Any](df.columns)
    if missing_columns:
        raise KeyError(f"DataFrame is missing required columns: {missing_columns}")
    
    ordered = df[columns]
    rows: list[tuple[Any, ...]] = list[tuple[Any, ...]](ordered.itertuples(index=False, name=None)) 
    sql = f"INSERT INTO {df_name} ({', '.join(columns)}) VALUES ({', '.join(values)})"

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.executemany(sql, rows) 
            conn.commit()
            logger.info(f"Successfully loaded {len(rows)} rows into {df_name} table")
    except sqlite3.IntegrityError as e:
        logger.error(f"Integrity error loading data into {df_name}: {e}")
        raise
    except sqlite3.Error as e:
        logger.error(f"Database error loading data into {df_name}: {e}")
        raise

def write_to_csv(df: pd.DataFrame, df_name: str, league_id: int, season_year: int) -> None:
    """
    Write DataFrame to CSV file.
    
    Args:
        df: DataFrame to write
        df_name: Base name for the CSV file
        league_id: League ID to include in filename
        season_year: Season year to include in filename
    """
    config = _load_config()
    processed_data_path = Path(config['paths']['processed_data'])
    processed_data_path.mkdir(parents=True, exist_ok=True)
    
    csv_path = processed_data_path / f"{df_name}_{league_id}_{season_year}.csv"
    df.to_csv(csv_path, index=False)
    logger.info(f"Successfully wrote {len(df)} rows to {csv_path}")

if __name__ == "__main__":
    leagues = pd.read_csv('processed_data/leagues.csv')
    load_data(leagues, "leagues")
    # pass