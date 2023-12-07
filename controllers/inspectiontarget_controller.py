from datetime import datetime

from fastapi import APIRouter, Depends
from starlette.responses import Response
from fastapi.security import OAuth2PasswordRequestForm
from fullstack_token.session import backend, cookie, verifier
from fastapi import Depends, HTTPException
from pydantic import BaseModel
from typing import Annotated
import models
from dtos.inspectiontarget import InspTargTypeRespItem, CreateInspTargTypeReq, InspTargTypesResp, CreateInspTargResp, CreateInspTargReq, InspectionTargetsResp, InspTargRespItem
from services.inspectiontarget_sqlalchemy import InspectionTargetService, InspectionTargetTypeService
from services.auth_sqlalchemy import AuthService, AuthServ
from dependencies import LoggedInUser


router = APIRouter(
    tags=['inspectiontarget'],
    prefix='/api/v1'
)

LoginForm = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/inspectiontarget/type', dependencies=[Depends(cookie)], response_model=InspTargTypeRespItem)
async def create_inspectiontarget_type(req: CreateInspTargTypeReq, authService: AuthServ, account: LoggedInUser, service: InspectionTargetTypeService = Depends(InspectionTargetTypeService)):
    if account.role != "admin":
        raise HTTPException(status_code=401, detail='unauthorized')
    else:
        type = service.create(req)
        return InspTargTypeRespItem(id=type.id, name=type.name)

@router.get('/inspectiontarget/type', dependencies=[Depends(cookie)], response_model=InspTargTypesResp)
async def get_inspectiontarget_types(authService: AuthServ, account: LoggedInUser, service: InspectionTargetTypeService = Depends(InspectionTargetTypeService)):
    types = service.get_all()
    types_resp_list = [{"id": type.id, "name": type.name} for type in types]
    return InspTargTypesResp(types=types_resp_list)

@router.post('/inspectiontarget', dependencies=[Depends(cookie)], response_model=CreateInspTargResp)
async def create_inspectiontarget(req: CreateInspTargReq, authService: AuthServ, account: LoggedInUser, service: InspectionTargetService = Depends(InspectionTargetService)):
    if account.role != "admin":
        raise HTTPException(status_code=401, detail='unauthorized')
    else:
        createdAt = datetime.now()
        createdAt = createdAt.strftime('%Y-%m-%d %H:%M:%S')
        it = service.create(req, createdAt)
        return CreateInspTargResp(id=it.id, name=it.name)

@router.get('/inspectiontargets', dependencies=[Depends(cookie)], response_model=InspectionTargetsResp)
async def get_inspectiontargets(authService: AuthServ, account: LoggedInUser, service: InspectionTargetService = Depends(InspectionTargetService)):
    inspectiontargets = service.get_all()
    inspectiontargets_resp_list = [{"id": it.id, "name": it.name} for it in inspectiontargets]
    return InspectionTargetsResp(inspectiontargets=inspectiontargets_resp_list)

@router.get('/inspectiontargets/{id}', dependencies=[Depends(cookie)], response_model=InspTargRespItem)
async def get_inspectiontarget_by_id(id: int, authService: AuthServ, account: LoggedInUser, service: InspectionTargetService = Depends(InspectionTargetService)):
    inspectiontarget = service.get_by_id(id)
    inspectiontarget_resp = InspTargRespItem(id=inspectiontarget.id, name=inspectiontarget.name)
    return inspectiontarget_resp

@router.get('/environment/{id}/inspectiontargets', dependencies=[Depends(cookie)], response_model=InspectionTargetsResp)
async def get_inspectiontargets_by_environment_id(id:int, authService: AuthServ, account: LoggedInUser, service: InspectionTargetService = Depends(InspectionTargetService)):
    inspectiontargets = service.get_inspectiontargets_by_environment_id(id)
    inspectiontargets_resp_list = [{"id": it.id, "name": it.name} for it in inspectiontargets]
    return InspectionTargetsResp(inspectiontargets=inspectiontargets_resp_list)
