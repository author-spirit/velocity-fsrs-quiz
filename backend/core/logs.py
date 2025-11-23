from core.config import Config
import logging

# Create logger
logger = logging.getLogger("velocity")

log_level = Config.get("log_level") or logging.INFO
log_file = Config.get("LOG_LOCATION") or "app.log"


logger.setLevel(log_level)

# File handler
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(log_level)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(log_level)

# Common format
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Attach handlers only once
if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
