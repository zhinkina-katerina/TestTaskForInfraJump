from typing import Any

from pydantic import BaseModel, Field, field_validator
from pydantic_core.core_schema import ValidationInfo


class Coordinates(BaseModel):
    lat: float = Field(..., ge=-90.0, le=90.0, description="Широта")
    lng: float = Field(..., ge=-180.0, le=180.0, description="Довгота")

    @field_validator("lat", "lng", mode="before")
    @classmethod
    def parse_str_coordinates(cls, v: Any, info: ValidationInfo) -> float:
        if isinstance(v, str):
            try:
                return float(v.strip())
            except ValueError:
                raise ValueError(f"{info.field_name} не може бути конвертовано у число")
        return v

    @classmethod
    def from_string(cls, coord_string: str) -> "Coordinates":
        try:
            lat_str, lng_str = coord_string.split(",")
            return cls(lat=float(lat_str.strip()), lng=float(lng_str.strip()))
        except Exception:
            raise ValueError("Неправильний формат координат: очікується 'lat, lng'")


class City(BaseModel):
    name: str
    description: str
    coordinates: Coordinates