import redis
import json

# Configure Redis connection
redis_client = redis.StrictRedis(
    host="localhost",  # Replace with your Redis server address
    port=6379,
    db=0,
    decode_responses=True  # Decode responses to strings
)

def get_cached_rates(cache_key: str):
    """
    Retrieve cached rates from Redis.
    :param cache_key: The unique cache key.
    :return: The cached data as a dictionary or None if not found.
    """
    cached_data = redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)
    return None

def set_cached_rates(cache_key: str, citylink_rate: float, jt_rate: float, expiration: int = 3600):
    """
    Cache rates in Redis with an expiration time.
    :param cache_key: The unique cache key.
    :param citylink_rate: CityLink rate to cache.
    :param jt_rate: J&T rate to cache.
    :param expiration: Expiration time in seconds (default: 1 hour).
    """
    data = {"citylink_rate": citylink_rate, "jt_rate": jt_rate}
    redis_client.setex(cache_key, expiration, json.dumps(data))
