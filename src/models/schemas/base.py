import datetime
import typing

from pydantic import BaseModel, BaseConfig, Extra

from src.utils.formatters.datetime_formatter import format_datetime_into_isoformat
from src.utils.formatters.field_formatter import format_dict_key_to_camel_case


__all__ = ['BaseOutSchemaModel', 'BaseInSchemaModel']


class BaseOutSchemaModel(BaseModel):
    class Config(BaseConfig):
        orm_mode: bool = True
        validate_assignment: bool = True
        allow_population_by_field_name: bool = True
        json_encoders: dict = {datetime.datetime: format_datetime_into_isoformat}
        alias_generator: typing.Any = format_dict_key_to_camel_case


class BaseInSchemaModel(BaseModel):

    class Config(BaseConfig):
        extra = Extra.forbid
        allow_population_by_field_name: bool = True
        json_encoders: dict = {datetime.datetime: format_datetime_into_isoformat}
        alias_generator: typing.Any = format_dict_key_to_camel_case
