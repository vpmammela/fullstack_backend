from pydantic import BaseModel
from typing import List

class CreateLocationReq(BaseModel):
    name: str
    address: str
    zipcode: str
    city: str

class CreateLocationResp(BaseModel):
    id: int
    name: str

class LocationRespItem(BaseModel):
    id: int
    name: str

class LocationsResp(BaseModel):
    locations: List[LocationRespItem]