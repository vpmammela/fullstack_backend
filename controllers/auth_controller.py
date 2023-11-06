import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import Response

import fullstack_token.token
import models
from dependencies import LoggedInUser
from dtos.auth import UserRegisterReq, UserRegisterRes, UserLoginRes, UserAccountRes
from services.auth_sqlalchemy import AuthService, AuthServ

router = APIRouter(
    tags=['auth'],
    prefix='/api/v1/auth'
)

LoginForm = Annotated[OAuth2PasswordRequestForm, Depends()]

@router.get('/account', response_model=UserAccountRes)
async def get_account(service: AuthServ, account: LoggedInUser):
    return account


@router.post('/register', response_model=UserRegisterRes)
async def register(req: UserRegisterReq, service: AuthServ):
    user = service.register(req)
    return {'username': user.email, 'firstName': user.firstName, 'lastName': user.lastName}



@router.post('/login', response_model=UserLoginRes)
async def login(service: AuthServ, login_form: LoginForm, _token: fullstack_token.token.Token, res: Response):
    csrf = str(uuid.uuid4())
    access, refresh, csrf_token = service.login(login_form.username, login_form.password, csrf, _token)

    if access is None and refresh is None and csrf_token is None:
        raise HTTPException(status_code=404, detail='user not found')
    res.set_cookie("access_token_cookie", access, secure=True, httponly=True)
    res.set_cookie("refresh_token_cookie", refresh, secure=True, httponly=True)
    res.set_cookie("csrf_token_cookie", csrf_token, secure=True, httponly=True)

    return {'access_token': access, 'refresh_token': refresh, 'csrf_token': csrf_token}

# ToDo
# Middleware joka tarkistaa että csrf_token_cookien 'sub' arvo on sama kuin access_tokenin 'csrf' arvo
# Tarvitaan SSL sertifikaatio, että saadaan cookiet käyttöön frontendissä
