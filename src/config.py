import yaml
from pathlib import Path
from typing import Dict, Any
from src.utils.logging import setup_logger

logger = setup_logger(__name__)

class Config:
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = Path(config_path)
        self.data = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(self.config_path, "r") as f:
                config = yaml.safe_load(f)
            logger.info(f"Loaded configuration from {self.config_path}")
            return config
        except FileNotFoundError:
            logger.error(f"Config file not found at {self.config_path}")
            raise
        except Exception as e:
            logger.error(f"Error loading config: {str(e)}")
            raise

    def get(self, key: str, default: Any = None) -> Any:
        """Get config value using dot notation (e.g., 'app.name')."""
        keys = key.split(".")
        value = self.data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

# Global config instance
try:
    # Assuming run from root
    config = Config()
except Exception:
    # Fallback to absolute path or relative from src if needed
    # For now, we assume execution from root
    pass
