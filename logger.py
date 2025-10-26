import os

import logging
from logging.handlers import RotatingFileHandler

# Create logs directory
os.makedirs("logs", exist_ok=True)

# Configure the logger
logger = logging.getLogger("scrape_logger")
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# File handler (rotating logs, up to 5 files of 1MB each)
file_handler = RotatingFileHandler("logs/scraper.log", maxBytes=1_000_000, backupCount=5)
file_handler.setLevel(logging.INFO)

# Format for logs
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    "%Y-%m-%d %H:%M:%S"
)

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Attach handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)



