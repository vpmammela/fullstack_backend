from pydantic import BaseModel
from typing import List
from datetime import datetime

class CreateInspResReq(BaseModel):
    value: int
    note: str
    title: str
    inspection_type: str

class CreateInspResResp(BaseModel):
    id: int
    title: str
