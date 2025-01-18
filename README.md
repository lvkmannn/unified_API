# **Testing the API Middleware - Unified API**

## **Overview**
The Unified API Middleware provides a robust solution for calculating postage rates by integrating multiple courier services.

At this moment, the API supports **domestic postage within Malaysia only (CityLink, Poslaju and J&T)**. In future updates, it will support **international postage** for various couriers.

---

## **Table of Contents**
1. [Prerequisites](#prerequisites)
2. [Running the Middleware](#1-running-the-middleware)
   - [Option 1: Run Locally](#option-1-run-locally)
   - [Option 2: Run in Docker](#option-2-run-in-docker)
3. [Testing the API](#2-testing-the-api)
   - [Manual Testing](#manual-testing)
   - [Automated Testing](#automated-testing)
4. [Debugging and Logs](#3-debugging-and-logs)
5. [Handling Common Issues](#4-handling-common-issues)
   - [Redis Connection Issues](#redis-connection-issues)
   - [Docker Issues](#docker-issues)
   - [API Validation Errors](#api-validation-errors)
6. [Clean Up](#5-clean-up)
7. [Cache Mechanism](#6-cache-mechanism)
8. [API Security](#7-api-security)
   - [Rate Limiting](#rate-limiting)
   - [API Versioning](#api-versioning)
9. [Additional Resources](#additional-resources)

---

## **Prerequisites**

1. **Environment Setup**:
   - Python installed (version 3.12 or higher).
   - Docker and Docker Compose installed.
   - Redis installed locally or running in a container.

2. **Clone the Repository**:
   - GitHub:
     ```bash
     git clone https://github.com/lvkmannn/unified_API.git
     ```

3. **Install Dependencies**:
   ```bash
   cd unified_API
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
   pip install -r requirements.txt


***

# 1. Running the Middleware
## Option 1: Run Locally

   1. Ensure Redis is running:
      * Locally: 
         ```bash
         sudo systemctl status redis-server
      * If it's not running: 
         ```bash
         sudo systemctl start redis-server

   2. Start the FastAPI server:
         ```bash
         uvicorn app.main:app --reload --port 8080

   3. Verify the server is running:
         * Visit: http://127.0.0.1:8080/

## Option 2: Run in Docker

   1. Build and start containers:
         ```bash
         docker-compose up --build

   2. Verify containers are running:
         ```bash
         docker ps

   3. Verify the server is running:
         * Visit: http://127.0.0.1:8080/


***


# 2. Testing the API
## Manual Testing
Use tools like **Postman** or **cURL** to test the API endpoints.

**API endpoint**: http://127.0.0.1:8080/api/v1/get-rates

Request:
```
curl -X POST http://127.0.0.1:8080/api/v1/get-rates \
-H "Content-Type: application/json" \
-d '{
    "package_type": "parcel",
    "origin": {
        "postcode": "77400",
        "state": "Johor"
    },
    "destination": {
        "postcode": "47130",
        "state": "Selangor"
    },
    "package": {
        "weight": 24,
        "dimensions": {
            "length": 1,
            "width": 2,
            "height": 3
        }
    }
}
```

Response:
```
{
    "data": [
        {
            "courier": "citylink",
            "rate": 53.0
        },
        {
            "courier": "jt",
            "rate": 46.64
        },
        {
            "courier": "poslaju",
            "rate": 59.91
        }
    ]
}
```

## Automated Testing
1. Run unit tests:
```
pytest
```

2. Sample output:
```
=============================== test session starts ===============================
platform win32 -- Python 3.12.3, pytest-8.3.4, pluggy-1.5.0
rootdir: D:\{your_directory}\Project\unified_API
configfile: pytest.ini
plugins: anyio-4.8.0, asyncio-0.25.2, time-machine-2.16.0
asyncio: mode=Mode.STRICT, asyncio_default_fixture_loop_scope=None
collected 4 items

app\tests\test_rates.py ....                                                                                                                                                                                      [100%]

=============================== 4 passed in 3.09s =============================== 
```


***


## 3. Debugging and Logs
Logs are generated in the `logs/` directory, named by date `(YYYY-MM-DD.log)`.
- View logs in real-time:
```
tail -f logs/2025-01-18.log
```


***


## 4. Handling Common Issues
### Redis Connection Issues
Ensure Redis is running locally or in a container:
```bash
redis-cli ping
```
Expected response:
```
PONG
```
### Docker Issues
If containers conflict, remove existing ones:
```
docker ps -a
docker rm <container-id>
```
### API Validation Errors
Ensure the payload matches the schema defined in unified.py. Below are the key validation rules:

**Validation Rules**
1. `package_type:`
   * Must be either `"parcel"` or `"document"`.
   * Example:
   ```
   "package_type": "parcel"
   ```
2. `origin` and `destination`:

   * `postcode`:

      * Must be a 5-digit number (e.g., `"47130"`).
      * Example:

      ```
      "postcode": "47130"
      ```

   * `postcode`:

      * Must be one of the valid Malaysian states:

      ```
      Johor, Kedah, Kelantan, Malacca, Melaka, Negeri Sembilan, Pahang, 
      Penang, Pulau Pinang, Perak, Perlis, Sabah, Sarawak, Selangor, 
      Terengganu, Kuala Lumpur, Labuan, Putrajaya
      ```

      * Example:

      ```
      "state": "Selangor"
      ```

3. `package`:

      * `weight`:

         * Must be a positive number.
         * Maximum: `30 kg `(applies to J&T and Poslaju).
         * Example:
         ```
         "weight": 15.5
         ```

      * `dimensions`:

         * Required. Must be a positive number.
         * `length`, `width`, `height`— all positive numbers.
         * Example:
         ```
         "dimensions": {
             "length": 1,
             "width": 2,
             "height": 3
         }
         ```

      * `item_value`:
         * Optional field for J&T insurance cover.
         * Rate will vary for J&T only if the user set the item value.

**Example Valid Payload:**
```
{
    "package_type": "parcel",
    "origin": {
        "postcode": "77400",
        "state": "Johor"
    },
    "destination": {
        "postcode": "47130",
        "state": "Selangor"
    },
    "package": {
        "weight": 24,
        "dimensions": {
            "length": 1,
            "width": 2,
            "height": 3
        },
        "item_value": 1000 # Optional
    }
}
```



***


## 5. Clean Up
1. Stop containers:
```
docker-compose down
```

2. Deactivate virtual environment:
```
deactivate
```



***


## 6. Cache Mechanism
The middleware uses Redis for caching. Here's how it works:
   1. Key Generation:
      * Cache keys are generated based on the request payload. Example:

      ```
      parcel:77400-47130:24.0:1x2x3:1000.0
      ```

   2. Cache Lookup:
      * Before making API calls to couriers, the middleware checks if a response is cached.

   3. Expiration:
      * Cached data expires after a predefined duration (in this project: 60 minutes)

   3. Advantages:
      * Reduces redundant API calls.
      * Improves response times for repeated requests.



***


## 7. API Security
**Rate Limiting**

   1. Implementation:
      * A rate limiter is integrated using Redis.
      * Each client IP is limited to 10 requests per minute.

   2. How It Works:
      * If the limit is exceeded, the API responds with:
      ```
      {
         "error": "Too many requests",
         "message": "Please try again later.",
         "retry_after": 60
      }
      ```

   3. Advantages:
      * Stops attackers or malicious users from overwhelming your API with excessive requests (e.g., brute force attacks or Denial of Service attacks).

**API Versioning**
   1. Current Version:
      * The middleware uses versioning in the URL (`/api/v1`).
      * A rate limiter is integrated using Redis.

   2. Advantages:
      * Backward Compatibility: Ensures older clients can continue using the API while you implement secure updates or deprecate outdated methods.
      * Enhanced Risk Management: Segregates different versions of the API, allowing you to apply stricter security policies or monitoring to specific versions.
      * Compliance with Security Standards: Keeps APIs compliant with modern security standards by rolling out versioned improvements.


---

## **Future Plans**
- **International Postage Support**:
  - Expand API functionality to handle international deliveries based on courier.

- **New Features**:
  - Dynamic rate calculation for insurance coverage.
  - Integration with additional couriers.

---

## **Contributing**
Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new feature branch.
3. Submit a pull request with a detailed explanation.

---

## **Contact**
For questions, issues, or suggestions, please open an issue on [GitHub](https://github.com/lvkmannn/unified_API/issues) or email me at `lnhafizramli@gmail.com`.


## Additional Resources
* API Documentation: Access auto-generated docs:
   * Swagger UI: http://127.0.0.1:8080/docs