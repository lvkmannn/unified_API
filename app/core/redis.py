import redis
import os
from dotenv import load_dotenv

# Load environment variable from .env file
load_dotenv()

# Get Redis credentials from environment variables
CACHE_HOST = os.getenv('REDIS_HOST')
CACHE_PORT = os.getenv('REDIS_PORT')

# Check if environment variables are set
if not all([CACHE_HOST, CACHE_PORT]):
    raise ValueError("Missing one or more environment variables for Redis connection")

# Configure Redis connection
redis_client = redis.StrictRedis(
    host=CACHE_HOST,
    port=CACHE_PORT,
    db=0,
    decode_responses=True  # Decode responses to strings
)
