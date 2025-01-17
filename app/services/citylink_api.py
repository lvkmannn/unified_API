import httpx
from app.core.logging_config import logger

async def fetch_citylink_rate(payload: dict) -> float:
    logger.info("Fetching CityLink rate")
    GET_URL = "https://www.citylinkexpress.com/wp-json/wp/v2/getShippingRate"

    async with httpx.AsyncClient() as client:
        response = await client.post(GET_URL, json=payload)
        logger.debug(f"POST request to {GET_URL} returned status code {response.status_code}")

        response.raise_for_status()
        data = response.json()
        
        rate = data.get("req", {}).get("data", {}).get("rate")
        if rate is None:
            logger.error("CityLink rate not found in response")
            raise ValueError("CityLink rate not found in response")
        return float(rate)
