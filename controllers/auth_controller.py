from typing import Annotated

from fastapi import APIRouter, Depends

import models
from dtos.auth import UserRegisterReq, UserRegisterRes
from services.auth_sqlalchemy import AuthService

router = APIRouter()

def get_auth_service(db: models.Db):
    return AuthService(db)


AuthServ = Annotated[AuthService, Depends(get_auth_service)]


@router.post('/api/v1/auth/register', response_model=UserRegisterRes)
async def register(req: UserRegisterReq, service: AuthServ):
    user = service.register(req)
    return {'username': user.email, 'firstName': user.firstName, 'lastName': user.lastName}



@router.post('/api/v1/auth/login')
async def login():
    return {'hello': 'from login'}