import httpx

async def fetch_citylink_rate(payload: dict) -> float:
    url = "https://www.citylinkexpress.com/wp-json/wp/v2/getShippingRate"
    async with httpx.AsyncClient() as client:
        print("City Link Payload: ", payload)

        response = await client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        
        rate = data.get("req", {}).get("data", {}).get("rate")
        if rate is None:
            raise ValueError("CityLink rate not found in response")
        return float(rate)
