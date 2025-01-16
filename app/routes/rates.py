from fastapi import APIRouter, HTTPException
from app.services.citylink_api import fetch_citylink_rate
from app.services.jnt_api import fetch_jt_rate
from app.schemas.unified import ShippingRequest
from app.utils.payload import create_citylink_payload, create_jt_payload

router = APIRouter()

@router.post("/get-rates")
async def get_shipping_rates(unified_input: ShippingRequest):
    try:
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

