from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class InspFormRespItem(BaseModel):
    id: int
    environment_id: Optional[int]
    inspectiontarget_id: Optional[int]
    inspectiontype_id: int

class InspFormReq(BaseModel):
    environment_id: Optional[int] = None
    inspectiontarget_id: Optional[int] = None
    inspectiontype: str

class FileResponseModel(BaseModel):
    random_name: str
    original_name: str
    id: int
    inspectionform_id: int

class InspectionformResponseModel(BaseModel):
    createdAt: datetime
    user_id: int
    inspectiontarget_id: int
    id: int
    closedAt: Optional[str] = None
    environment_id: Optional[int] = None
    inspectiontype_id: int
    files: Optional[List[FileResponseModel]] = None