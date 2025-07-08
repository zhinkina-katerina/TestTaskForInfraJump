from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime

class QueryCreate(BaseModel):
    city: str
    text: str
    exclude: Optional[List[str]]
    num_places: Optional[int] = 3

# app/schemas/query.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ResponseItem(BaseModel):
    name: str
    description: Optional[str]
    country: Optional[str]
    url: Optional[str]
    coordinates: dict  # {'lat': ..., 'lng': ...}

    @classmethod
    def from_model(cls, obj):
        return cls(
            name=obj.name,
            description=obj.description,
            country=obj.country,
            url=obj.url,
            coordinates={"lat": obj.lat, "lng": obj.lon}
        )


class QueryOut(BaseModel):
    id: int
    city: str
    text: str
    num_places: int
    exclude: List[str]
    response_json: List[ResponseItem]
    created_at: datetime

    @classmethod
    def from_model(cls, query):
        return cls(
            id=query.id,
            city=query.city,
            text=query.text,
            num_places=query.num_places,
            exclude=[e.name for e in query.excludes],
            response_json=[ResponseItem.from_model(r) for r in query.responses],
            created_at=query.created_at
        )

