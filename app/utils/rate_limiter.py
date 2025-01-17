import time
from app.core.redis import redis_client

def is_rate_limited(client_id: str, max_requests: int, window_seconds: int) -> bool:
    """
    Check if the client has exceeded the rate limit.
    :param client_id: A unique identifier for the client (e.g., IP address or API key).
    :param max_requests: Maximum number of requests allowed within the time window.
    :param window_seconds: Time window in seconds.
    :return: True if rate-limited, False otherwise.
    """
    # Create a unique Redis key for the client and time window
    current_time = int(time.time())
    key = f"rate_limit:{client_id}:{current_time // window_seconds}"

    # Increment the count for this key
    request_count = redis_client.incr(key)

    # Set the TTL (time to live) for the key on the first request
    if request_count == 1:
        redis_client.expire(key, window_seconds)

    # Check if the client has exceeded the limit
    return request_count > max_requests
