import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

# Generate log file name using date
LOG_FILE = f"logs/{datetime.now().strftime('%Y-%m-%d')}.log"

# Ensure the logs directory exists
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level
    format="%(asctime)s [%(levelname)s] %(message)s",  # Log message format
    handlers=[
        logging.StreamHandler(),  # Log to console
        RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3),  # Log to file with rotation
    ],
)

# Create a logger instance
logger = logging.getLogger("app_logger")