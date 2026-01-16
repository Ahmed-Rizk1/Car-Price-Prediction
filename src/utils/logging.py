import logging
import sys
from pathlib import Path

def setup_logger(name: str = "app_logger", log_file: str = "app.log", level=logging.INFO):
    """Function to setup a logger; can be used across the application."""
    
    # Create a custom logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid adding handlers multiple times in Streamlit
    if not logger.handlers:
        # Create handlers
        c_handler = logging.StreamHandler(sys.stdout)
        f_handler = logging.FileHandler(log_file)
        
        c_handler.setLevel(level)
        f_handler.setLevel(level)

        # Create formatters and add it to handlers
        c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)

        # Add handlers to the logger
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)
        
    return logger
