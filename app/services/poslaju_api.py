import httpx
from app.core.logging_config import logger

async def fetch_poslaju_rate(payload: dict) -> float:
    logger.info("Fetching Poslaju rate")
    GET_URL = "https://www-api.pos.com.my/api/price"

    async with httpx.AsyncClient() as client:
        response = await client.post(GET_URL, json=payload)
        logger.debug(f"POST request to {GET_URL} returned status code {response.status_code}")

        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and len(data) > 0:
            rate = data[0].get("totalAmount")
            if rate is None:
                logger.error("Total amount not found in Poslaju response")
                raise ValueError("Total amount not found in Poslaju response")
            logger.info(f"Poslaju Rate: {rate}")
            return float(rate)
        else:
            logger.error(f"Unexpected Poslaju API response structure: {data}")
            raise ValueError("Unexpected Poslaju API response structure")