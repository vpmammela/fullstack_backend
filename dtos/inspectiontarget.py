from pydantic import BaseModel
from typing import List
from datetime import datetime

class CreateInspTargReq(BaseModel):
    name: str
    description: str
    createdAt: datetime
    environment_id: int
    inspectiontargettype_id: int

class CreateInspTargTypeReq(BaseModel):
    name: str

class CreateInspTargResp(BaseModel):
    id: int
    name: str

class InspTargRespItem(BaseModel):
    id: int
    name: str

class InspectionTargetsResp(BaseModel):
    inspectiontargets: List[InspTargRespItem]

class InspTargTypeRespItem(BaseModel):
    id: int
    name: str

class InspTargTypesResp(BaseModel):
    types: List[InspTargTypeRespItem]