from fastapi import APIRouter, HTTPException
from app.services.citylink_api import fetch_citylink_rate
from app.services.jnt_api import fetch_jt_rate
from app.schemas.unified import ShippingRequest
from app.utils.payload import create_citylink_payload, create_jt_payload
from app.utils.cache import get_cached_rates, set_cached_rates

router = APIRouter()

@router.post("/get-rates")
async def get_shipping_rates(unified_input: ShippingRequest):

    try:
        # Generate a unique cache key based on the request
        cache_key = f"{unified_input.shipping_type}:{unified_input.package_type}:" \
                    f"{unified_input.origin.country}-{unified_input.origin.postcode}:" \
                    f"{unified_input.destination.country}-{unified_input.destination.postcode}:" \
                    f"{unified_input.package.weight}:" \
                    f"{unified_input.package.dimensions.get('length', '')}x" \
                    f"{unified_input.package.dimensions.get('width', '')}x" \
                    f"{unified_input.package.dimensions.get('height', '')}:" \
                    f"{unified_input.jnt_shipping_type}:" \
                    f"{unified_input.package.item_value if unified_input.package.item_value is not None else '0'}"

        
         # Check if rates are cached
        cached_rates = get_cached_rates(cache_key)
        if cached_rates:
            print("Cache hit for key:", cache_key)
            return {
                "data": [
                    {"courier": "citylink", "rate": cached_rates["citylink_rate"]},
                    {"courier": "jt", "rate": cached_rates["jt_rate"]}
                ]
            }
        
        print("Cache miss for key:", cache_key)

        # Convert the parsed model into a dictionary for further processing
        input_data = unified_input.dict()

        # Generate payloads
        citylink_payload = create_citylink_payload(input_data)
        jt_payload = create_jt_payload(input_data)

        # Fetch rates for CityLink
        citylink_rate = await fetch_citylink_rate(citylink_payload)

        # Fetch rates for J&T
        package_type = input_data.get("package_type", "parcel")  # Default to parcel if not specified
        jt_rate = fetch_jt_rate(jt_payload, package_type=package_type)

        # Cache the results
        set_cached_rates(cache_key, citylink_rate, jt_rate)

        # Construct the JSON response
        response = {
            "data": [
                {"courier": "citylink", "rate": citylink_rate},
                {"courier": "jt", "rate": jt_rate},
            ]
        }

        return response

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

