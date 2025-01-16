

def create_citylink_payload(unified_input: dict) -> dict:
    package_type = unified_input["package_type"]
    package = unified_input["package"]

    payload = {
        "origin_country": unified_input["origin"]["country"],
        "origin_state": unified_input["origin"]["state"],
        "origin_postcode": unified_input["origin"]["postcode"],
        "destination_country": unified_input["destination"]["country"],
        "destination_state": unified_input["destination"]["state"],
        "destination_postcode": unified_input["destination"]["postcode"],
        "selected_type": 1 if package_type == "parcel" else 2,
        "parcel_weight": package["weight"] if package_type == "parcel" else None,
        "document_weight": package["weight"] if package_type == "document" else None,
        "length": package["dimensions"]["length"] if package_type == "parcel" else None,
        "width": package["dimensions"]["width"] if package_type == "parcel" else None,
        "height": package["dimensions"]["height"] if package_type == "parcel" else None,
    }

    # Add default values for international destinations
    if unified_input["shipping_type"] == "international":
        payload["destination_postcode"] = "50000"  # Default international postcode

    return payload


def create_jt_payload(unified_input: dict) -> dict:
    package = unified_input["package"]

    destination_country = (
        "BWN" if unified_input["shipping_type"] == "domestic" else unified_input["destination"]["country"]
    )

    payload = {
        "shipping_rates_type": unified_input["shipping_type"],
        "sender_postcode": unified_input["origin"]["postcode"],
        "receiver_postcode": unified_input["destination"]["postcode"],
        "destination_country": destination_country,
        "shipping_type": unified_input.get("jnt_shipping_type", "EZ"), 
        "weight": package["weight"],
        "length": package["dimensions"]["length"],
        "width": package["dimensions"]["width"],
        "height": package["dimensions"]["height"],
        "item_value": package.get("value", ""),  # Optional field for J&T
    }

    return payload

