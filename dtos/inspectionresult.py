from pydantic import BaseModel
from typing import List
from datetime import datetime

class CreateInspResReq(BaseModel):
    value: int
    note: str
    title: str
    inspectionform_id: int

class InspResResp(BaseModel):
    id: int
    title: str
    note: str

