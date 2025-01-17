import redis
import os
from dotenv import load_dotenv
from app.core.logging_config import logger

# Load environment variable from .env file
load_dotenv()

# Get Redis credentials from environment variables
CACHE_HOST = os.getenv('REDIS_HOST')
CACHE_PORT = os.getenv('REDIS_PORT')

# Check if environment variables are set
if not all([CACHE_HOST, CACHE_PORT]):
    logger.error("Missing one or more environment variables for Redis connection")
    raise ValueError("Missing one or more environment variables for Redis connection")

# Configure Redis connection
logger.info(f"Configuring Redis connection: host={CACHE_HOST}, port={CACHE_PORT}")
redis_client = redis.StrictRedis(
    host=CACHE_HOST,
    port=CACHE_PORT,
    db=0,
    decode_responses=True  # Decode responses to strings
)
