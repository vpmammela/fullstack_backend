from pydantic import BaseModel
from typing import List
from typing import Optional

class InspFormRespItem(BaseModel):
    id: int
    environment_id: Optional[int]
    inspectiontarget_id: Optional[int]
    inspectiontype_id: int

class InspFormReq(BaseModel):
    environment_id: Optional[int] = None
    inspectiontarget_id: Optional[int] = None
    inspectiontype: str
