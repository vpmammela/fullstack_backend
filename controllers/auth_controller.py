import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import Response

import fullstack_token.token
import models
from dependencies import LoggedInUser, AuthRes
from dtos.auth import UserRegisterReq, UserRegisterRes, UserLoginRes, UserAccountRes, SessionData
from fullstack_token.session import backend, cookie, verifier
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
async def login(service: AuthServ, login_form: LoginForm, _token: fullstack_token.token.Token, res: Response,
                res_handler: AuthRes):
    print("something is happening")
    csrf = str(uuid.uuid4())
    #access, refresh, csrf_token = service.login(login_form.username, login_form.password, csrf, _token)
    try:
        access, refresh, csrf_token = service.login(login_form.username, login_form.password, csrf, _token)
    except Exception as e:
        print(f"Exception in login: {e}")
        raise

    if access is None and refresh is None and csrf_token is None:
        raise HTTPException(status_code=404, detail='user not found')
    print(f"Login successful: access={access}, refresh={refresh}, csrf_token={csrf_token}")

    return await res_handler.send(res, access, refresh, csrf_token, '')

