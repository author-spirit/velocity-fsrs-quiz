from core.config import Config
from loguru import logger
import sys

# Get log file location and log level from config or set default
log_file = Config.get("LOG_LOCATION", "app.log")
log_level = Config.get("LOG_LEVEL", "INFO")

logger.remove()

logger.add(sys.stdout, level=log_level.upper())
logger.add(
    log_file,
    rotation="10 MB",                 # Rotate after 10 MB
    retention="10 days",              # Keep logs for 10 days
    compression="zip",                # Compress rotated logs
    backtrace=True,                   # Show backtrace on errors
    diagnose=True,                    # Detailed stacktrace
    enqueue=True,                     # For multiprocess safety
)

