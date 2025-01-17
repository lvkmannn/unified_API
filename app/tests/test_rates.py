import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)

@pytest.fixture
def mock_payload():
    return {
        "shipping_type": "domestic",
        "package_type": "parcel",
        "origin": {
            "country": "MY",
            "postcode": "40000",
            "state": "Selangor"
        },
        "destination": {
            "country": "MY",
            "postcode": "50000",
            "state": "Kuala Lumpur"
        },
        "package": {
            "weight": 10.5,
            "dimensions": {
                "length": 20,
                "width": 15,
                "height": 10
            },
            "item_value": 250.00
        },
        "jnt_shipping_type": "EZ"
    }

# Test rates valid input
def test_get_rates(mock_payload):
    response = client.post("/api/v1/get-rates", json=mock_payload)
    assert response.status_code == 200
    assert "data" in response.json()

# Test rates invalid input
def test_get_rates_invalid_payload():
    invalid_payload = {
        "shipping_type": "invalid_type"
    }
    response = client.post("/api/v1/get-rates", json=invalid_payload)
    assert response.status_code == 422

# Test rate limiter - within limit
@patch("app.utils.rate_limiter.redis_client")  # Mock Redis interactions
def test_rate_limiter_within_limit(mock_redis):
    """
    Test 10 requests within the limit.
    """
    # Mock Redis behavior
    mock_redis.incr.side_effect = lambda key: 1  # Simulate Redis increment
    mock_redis.expire.return_value = None  # Ignore expiration in the test

    # Simulate 10 requests
    for _ in range(10):
        response = client.get("/")
        assert response.status_code == 200  # All requests should pass

# Test rate limiter - exceed limit
@patch("app.utils.rate_limiter.redis_client")  # Mock Redis interactions
def test_rate_limiter_exceed_limit(mock_redis):
    """
    Test exceeding the rate limit of 10 requests per minute.
    """
    # Mock Redis behavior
    call_count = 0

    def mock_incr(key):
        nonlocal call_count
        call_count += 1
        return call_count

    mock_redis.incr.side_effect = mock_incr
    mock_redis.expire.return_value = None

    # Simulate 10 requests (within the limit)
    for i in range(10):
        response = client.get("/")
        assert response.status_code == 200, f"Failed on request {i + 1}"

    # Simulate 11th request (should fail)
    response = client.get("/")
    assert response.status_code == 429

    # Validate response content
    json_response = response.json()
    assert json_response == {
        "error": "Too many requests",
        "message": "Please try again later.",
        "retry_after": 60,
    }