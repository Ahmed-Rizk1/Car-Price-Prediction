import pandas as pd
from pathlib import Path
from src.config import config
from src.utils.logging import setup_logger

logger = setup_logger(__name__)

def load_dataset() -> pd.DataFrame:
    """
    Load the cleaned dataset from the path specified in config.
    Returns:
        pd.DataFrame: The loaded dataset.
    """
    data_path = config.get("paths.data")
    try:
        logger.info(f"Loading data from {data_path}")
        df = pd.read_csv(data_path)
        logger.info(f"Successfully loaded data with shape {df.shape}")
        return df
    except FileNotFoundError:
        logger.error(f"Data file not found at {data_path}")
        raise
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        raise
