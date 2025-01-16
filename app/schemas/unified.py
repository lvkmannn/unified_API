from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional

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
        },
        "jnt_shipping_type": "EX"
    }
    
    '''

class OriginDestination(BaseModel):
    country: str = Field(..., description="Country code, e.g., 'MY'")
    postcode: str = Field(..., description="Postcode for the location")
    state: str = Field(..., description="State Name, e.g., Selangor")
    
    # Field validator for country
    @field_validator("country")
    def validate_country(cls, value):
        if len(value) != 2:
            raise ValueError("Country code must be a 2-letter ISO code.")
        return value

class Package(BaseModel):
    weight: float
    dimensions: Optional[dict] = None
    value: Optional[float] = None

    # Validator for weight
    @field_validator("weight")
    def validate_weight(cls, value):

        print("Value in unified: ", value)
        if value <= 0:
            raise ValueError("Weight must be a positive number.")
        elif value > 30:
            raise ValueError("Weight must not exceed 30kg for J&T")
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
                raise ValueError("All dimensions (length, width, height) must be positive if provided.")
        return values


class ShippingRequest(BaseModel):
    shipping_type: str = Field(..., description="domestic or international")
    package_type: str = Field(..., description="parcel or document")
    origin: OriginDestination
    destination: OriginDestination
    package: Package
    jnt_shipping_type: Optional[str] = "EZ" 

    # Validator for shipping type
    @field_validator("shipping_type")
    def validate_shipping_type(cls, value):
        allowed_types = {"domestic", "international"}
        if value not in allowed_types:
            raise ValueError(f"Invalid shipping_type: {value}. Must be one of {allowed_types}.")
        return value

    # Validator for package type
    @field_validator("package_type")
    def validate_package_type(cls, value):
        allowed_types = {"parcel", "document"}
        if value not in allowed_types:
            raise ValueError(f"Invalid package type: {value}. Must be one of  {allowed_types}.")
        return value

