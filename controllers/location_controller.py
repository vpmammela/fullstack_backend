from fastapi import APIRouter, Depends
from starlette.responses import Response
from fastapi.security import OAuth2PasswordRequestForm
from fullstack_token.session import backend, cookie, verifier
from fastapi import Depends
from pydantic import BaseModel
from typing import Annotated
import models
from dtos.location import CreateLocationReq, CreateLocationResp
from services.location_sqlalchemy import LocationService

router = APIRouter(
    tags=['location'],
    prefix='/api/v1'
)

LoginForm = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/location', dependencies=[Depends(cookie)], response_model=CreateLocationResp)
async def create_location(req: CreateLocationReq, service: LocationService = Depends(LocationService)):
    location = service.create(req)
    return CreateLocationResp(id=location.id, name=location.name)
