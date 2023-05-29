from pydantic import Field

from .base import BaseOutSchemaModel


__all__ = ['TransportInUpdateSchema']


class TransportInUpdateSchema(BaseOutSchemaModel):
    post_code: str = Field(..., min_length=3, max_length=15)
