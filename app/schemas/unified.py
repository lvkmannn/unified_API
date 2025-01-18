from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional
from app.core.logging_config import logger

'''
Sample data for unified API

{
    "shipping_type": "domestic",
    "package_type": "document",
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
        "weight": 30,
        "dimensions": {
            "length": 1,
            "width": 1,
            "height": 1
        }
    }
}

'''

# Define valid Malaysian states
MALAYSIA_STATES = {
        "Johor", "Kedah", "Kelantan", "Malacca", "Melaka",
        "Negeri Sembilan", "Pahang", "Penang", "Pulau Pinang",
        "Perak", "Perlis", "Sabah", "Sarawak", "Selangor",
        "Terengganu", "Kuala Lumpur", "Labuan", "Putrajaya"
    }

class OriginDestination(BaseModel):
    postcode: str = Field(..., description="Postcode for the location")
    state: str = Field(..., description="State Name, e.g., Selangor")

    @field_validator("postcode")
    def validate_postcode(cls, value):
        if not value.isdigit() or len(value) != 5:
            logger.error(f"Invalid postcode: {value}. Must be a 5-digit number.")
            raise ValueError("Postcode must be a 5-digit number.")
        return value
    
    @field_validator("state")
    def validate_state(cls, value):
        if value not in MALAYSIA_STATES:
            logger.error(f"Invalid state: {value}. Must be one of {MALAYSIA_STATES}.")
            raise ValueError(f"Invalid state: {value}. Must be one of {MALAYSIA_STATES}.")
        return value

class Package(BaseModel):
    weight: float
    dimensions: Optional[dict] = None
    item_value: Optional[float] = None

    # Validator for weight
    @field_validator("weight")
    def validate_weight(cls, value):

        #print("Value in unified: ", value)
        if value <= 0:
            logger.error(f"Invalid weight: {value}. Must be positive.")
            raise ValueError("Weight must be a positive number.")
        elif value > 30:
            logger.warning(f"Weight exceeds limit for J&T and Poslaju: {value}kg.")
            raise ValueError("Weight must not exceed 30kg for J&T and Poslaju")
        return value

     # Validator for dimensions
    @model_validator(mode="after")
    def validate_dimensions(cls, values):
        dimensions = values.dimensions or {}

        length = dimensions.get("length")
        width = dimensions.get("width")
        height = dimensions.get("height")

        if any(dim is not None for dim in [length, width, height]):
            if not all(dim is not None and dim > 0 for dim in [length, width, height]):
                logger.error(f"Invalid dimensions: {dimensions}. All dimensions must be positive.")
                raise ValueError("All dimensions (length, width, height) must be positive if provided.")
        return values


class ShippingRequest(BaseModel):
    package_type: str = Field(..., description="parcel or document")
    origin: OriginDestination
    destination: OriginDestination
    package: Package
    jnt_shipping_type: Optional[str] = "EZ" 

    # Validator for package type
    @field_validator("package_type")
    def validate_package_type(cls, value):
        allowed_types = {"parcel", "document"}
        if value not in allowed_types:
            logger.error(f"Invalid package type: {value}. Must be one of {allowed_types}.")
            raise ValueError(f"Invalid package type: {value}. Must be one of  {allowed_types}.")
        return value

