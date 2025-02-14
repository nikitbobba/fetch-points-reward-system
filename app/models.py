from datetime import date, time

from pydantic import BaseModel, ConfigDict, Field


class Item(BaseModel):
    short_description: str = Field(
        ...,
        alias="shortDescription",
        pattern=r"^[\w\s\-]+$",
        description="The Short Product Description for the item.",
    )
    price: str = Field(
        ..., pattern=r"^\d+\.\d{2}$", description="The total price payed for this item."
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"shortDescription": "Mountain Dew 12PK", "price": "6.49"}
        }
    )


class Receipt(BaseModel):
    retailer: str = Field(
        ...,
        pattern=r"^[\w\s\-&]+$",
        description="The name of the retailer or store the receipt is from",
    )
    purchase_date: date = Field(..., alias="purchaseDate")
    purchase_time: time = Field(..., alias="purchaseTime")
    items: list[Item] = Field(..., min_length=1)
    total: str = Field(
        ...,
        pattern=r"^\d+\.\d{2}$",
        description="The total amount paid on the receipt.",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "retailer": "M&M Corner Market",
                "purchaseDate": "2022-01-01",
                "purchaseTime": "13:01",
                "total": "6.49",
            }
        }
    )


class ProcessReceiptResponse(BaseModel):
    id: str = Field(
        ..., pattern=r"^\S+$", description="Returns the ID assigned to the receipt."
    )

    model_config = ConfigDict(
        json_schema_extra={"example": {"id": "adb6b560-0eef-42bc-9d16-df48f30e89b2"}}
    )


class GetReceiptPointsResponse(BaseModel):
    points: int = Field(...)

    model_config = ConfigDict(json_schema_extra={"example": {"points": 100}})
