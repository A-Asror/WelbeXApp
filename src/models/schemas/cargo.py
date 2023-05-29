import datetime as dt

from decimal import Decimal, ROUND_DOWN

from pydantic import Field, root_validator
from pydantic.class_validators import validator
from geopy.distance import geodesic

from .base import BaseOutSchemaModel, BaseInSchemaModel

__all__ = [
    'CargoInCreateSchema',
    'CargoInUpdateSchema',
    'CargoInQueryParamsSchema',
    'CargoOutMainInfoSchema',
    'CargoOutListMinInfoSchema',
    'CargoInfoOutSchema',
    'CargoFilterByRadiusWeightOutSchema',
]


class CargoOutMainInfoSchema(BaseOutSchemaModel):
    id: int
    pick_up_lat: float
    pick_up_lng: float
    delivery_lat: float
    delivery_lng: float
    weight: float
    description: str
    created_at: dt.datetime
    updated_at: dt.datetime


class CargoOutListMinInfoSchema(BaseOutSchemaModel):
    id: int
    pick_up_post_code: str = Field(..., alias='pick_up')
    delivery_post_code: str = Field(..., alias='delivery')
    transports: int | None = Field(None, alias='count_transports')


class CargoInfoTransportsSchema(BaseOutSchemaModel):
    id: int | None = None
    location_lat: float
    location_lng: float
    transport_number: str | None = None
    distance: float | Decimal | None = None

    @validator('distance')
    def validate_distance(cls, v: float):
        return Decimal(str(v)).quantize(Decimal('0.00'), rounding=ROUND_DOWN)


class CargoInfoOutSchema(BaseOutSchemaModel):
    id: int
    pick_up_post_code: str = Field(..., alias='pick_up')
    delivery_post_code: str = Field(..., alias='delivery')
    weight: float
    description: str | None = None
    transports: list[CargoInfoTransportsSchema]

    def distance(self, lat: float, lng: float):
        cargo_location = (lat, lng)

        for transport in self.transports:
            transport_location = (transport.location_lat, transport.location_lng)
            transport.distance = geodesic(cargo_location, transport_location).miles


class CargoFilterByRadiusWeightOutSchema(BaseOutSchemaModel):
    id: int
    pick_up_post_code: str = Field(..., alias='pick_up')
    delivery_post_code: str = Field(..., alias='delivery')
    weight: float
    description: str | None = None
    transports: int | None = None


class CargoInCreateSchema(BaseInSchemaModel):
    pick_up: str
    delivery: str
    weight: float = Field(..., ge=1, le=1000)
    description: str = Field(..., max_length=7000)


class CargoInUpdateSchema(BaseInSchemaModel):
    weight: float | None = Field(None, ge=1, le=1000)
    description: str | None = Field(None, max_length=7000)


class CargoInQueryParamsSchema(BaseInSchemaModel):
    weight: float | None = Field(None, ge=1, le=1000)
    radius: int | None = Field(None, ge=5)
    page: int = Field(1, ge=1)

