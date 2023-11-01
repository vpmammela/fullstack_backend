from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

import fullstack_token.token
import models
from dtos.auth import UserRegisterReq, UserRegisterRes, UserLoginRes
from services.auth_sqlalchemy import AuthService

router = APIRouter(
    tags=['auth'],
    prefix='/api/v1/auth'
)

LoginForm = Annotated[OAuth2PasswordRequestForm, Depends()]

def get_auth_service(db: models.Db):
    return AuthService(db)


AuthServ = Annotated[AuthService, Depends(get_auth_service)]


@router.post('/register', response_model=UserRegisterRes)
async def register(req: UserRegisterReq, service: AuthServ):
    user = service.register(req)
    return {'username': user.email, 'firstName': user.firstName, 'lastName': user.lastName}



@router.post('/login', response_model=UserLoginRes)
async def login(service: AuthServ, login_form: LoginForm, _token: fullstack_token.token.Token):
    access, refresh = service.login(login_form.username, login_form.password, _token)
    if access is None and refresh is None:
        raise HTTPException(status_code=404, detail='user not found')
    return {'access_token': access, 'refresh_token': refresh}
