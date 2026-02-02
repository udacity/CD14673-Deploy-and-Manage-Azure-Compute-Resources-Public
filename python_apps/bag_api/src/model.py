from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal

import uuid

class APIGWParameters(BaseModel):
    flight_number: str
    bag_id: Optional[str] = None

class APIGWEvent(BaseModel):
    pathParameters: APIGWParameters

class Location(BaseModel):
    lat: Decimal
    lon: Decimal
    description: str
    timestamp: datetime = datetime.now()
    code: str

class Person(BaseModel):
    id: str = str(uuid.uuid4())
    first_name: str
    last_name: str


class Checked_Bag(BaseModel):
    id: str = str(uuid.uuid4())
    customer: Person
    desk_agent: Person
    current_location: Location
    location_history: list[Location] = []
    checked_in: bool = False
    retrieved: bool = False
    flight_number: str
    created: datetime
    updated: datetime