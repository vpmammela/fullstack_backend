from fastapi import APIRouter, Depends
from starlette.responses import Response
from fastapi.security import OAuth2PasswordRequestForm
from fullstack_token.session import backend, cookie, verifier
from fastapi import Depends, HTTPException
from pydantic import BaseModel
from typing import Annotated
import models
from dtos.location import CreateLocationReq, CreateLocationResp
from services.location_sqlalchemy import LocationService
from services.auth_sqlalchemy import AuthService, AuthServ
from dependencies import LoggedInUser


router = APIRouter(
    tags=['location'],
    prefix='/api/v1'
)

LoginForm = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/location', dependencies=[Depends(cookie)], response_model=CreateLocationResp)
async def create_location(req: CreateLocationReq, authService: AuthServ, account: LoggedInUser, service: LocationService = Depends(LocationService)):
    if account.role != "admin":
        raise HTTPException(status_code=401, detail='unauthorized')
    else:
        location = service.create(req)
        return CreateLocationResp(id=location.id, name=location.name)
