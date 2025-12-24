from core.config import Config
import logging

# Get log level and file location from config
log_file = Config.get("LOG_LOCATION", "app.log")

logging.basicConfig(
    level=Config.get("log_level", logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("velocity")
