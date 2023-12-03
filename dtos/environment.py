from pydantic import BaseModel
from typing import List

class CreateEnvReq(BaseModel):
    name: str
    description: str
    location_id: int
    environmenttype_id: int

class CreateEnvTypeReq(BaseModel):
    name: str

class CreateEnvResp(BaseModel):
    id: int
    name: str

class EnvRespItem(BaseModel):
    id: int
    name: str

class EnvironmentsResp(BaseModel):
    environments: List[EnvRespItem]

class EnvTypeRespItem(BaseModel):
    id: int
    name: str

class EnvTypesResp(BaseModel):
    types: List[EnvTypeRespItem]
