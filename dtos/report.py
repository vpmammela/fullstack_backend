from typing import List, Optional
from pydantic import BaseModel

class InspectionformResponse(BaseModel):
    createdAt: str
    user_id: int
    inspectiontarget_id: Optional[int]
    id: int
    closedAt: Optional[str]
    environment_id: Optional[int]
    inspectiontype_id: int

class InspectionresultResponse(BaseModel):
    id: int
    note: str
    inspectionform_id: int
    createdAt: str
    value: int
    title: str
    inspectionform: InspectionformResponse

class InspectionresultListResponse(BaseModel):
    items: List[InspectionresultResponse]
