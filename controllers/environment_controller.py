from fastapi import APIRouter, Depends
from starlette.responses import Response
from fastapi.security import OAuth2PasswordRequestForm
from fullstack_token.session import backend, cookie, verifier
from fastapi import Depends, HTTPException
from pydantic import BaseModel
from typing import Annotated
import models
from dtos.environment import EnvTypeRespItem, CreateEnvTypeReq, EnvTypesResp, CreateEnvResp, CreateEnvReq, EnvironmentsResp, EnvRespItem
from services.environment_sqlalchemy import EnvironmentTypeService, EnvironmentService
from services.auth_sqlalchemy import AuthService, AuthServ
from dependencies import LoggedInUser


router = APIRouter(
    tags=['environment'],
    prefix='/api/v1'
)

LoginForm = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/environment/type', dependencies=[Depends(cookie)], response_model=EnvTypeRespItem)
async def create_environment_type(req: CreateEnvTypeReq, authService: AuthServ, account: LoggedInUser, service: EnvironmentTypeService = Depends(EnvironmentTypeService)):
    if account.role != "admin":
        raise HTTPException(status_code=401, detail='unauthorized')
    else:
        type = service.create(req)
        return EnvTypeRespItem(id=type.id, name=type.name)

@router.get('/environment/type', dependencies=[Depends(cookie)], response_model=EnvTypesResp)
async def get_environment_types(authService: AuthServ, account: LoggedInUser, service: EnvironmentTypeService = Depends(EnvironmentTypeService)):
    types = service.get_all()
    types_resp_list = [{"id": type.id, "name": type.name} for type in types]
    return EnvTypesResp(types=types_resp_list)

@router.post('/environment', dependencies=[Depends(cookie)], response_model=CreateEnvResp)
async def create_environment(req: CreateEnvReq, authService: AuthServ, account: LoggedInUser, service: EnvironmentService = Depends(EnvironmentService)):
    if account.role != "admin":
        raise HTTPException(status_code=401, detail='unauthorized')
    else:
        env = service.create(req)
        return CreateEnvResp(id=env.id, name=env.name)

@router.get('/environments', dependencies=[Depends(cookie)], response_model=EnvironmentsResp)
async def get_environments(authService: AuthServ, account: LoggedInUser, service: EnvironmentService = Depends(EnvironmentService)):
    environments = service.get_all()
    environments_resp_list = [{"id": env.id, "name": env.name} for env in environments]
    return EnvironmentsResp(environments=environments_resp_list)

@router.get('/environments/{id}', dependencies=[Depends(cookie)], response_model=EnvRespItem)
async def get_environment_by_id(id: int, authService: AuthServ, account: LoggedInUser, service: EnvironmentService = Depends(EnvironmentService)):
    environment = service.get_by_id(id)
    environment_resp = EnvRespItem(id=environment.id, name=environment.name)
    return environment_resp

@router.get('/locations/{id}/environments', dependencies=[Depends(cookie)], response_model=EnvironmentsResp)
async def get_environments_by_location_id(id: int, service: EnvironmentService = Depends(EnvironmentService)):
    environments = service.get_all_by_location_id(id)
    environments_resp_list = [{"id": env.id, "name": env.name} for env in environments]
    return EnvironmentsResp(environments=environments_resp_list)