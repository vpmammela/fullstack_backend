import os
from typing import Optional, Annotated

from fastapi import Depends, Cookie, HTTPException
from fastapi.security import OAuth2PasswordBearer

import models
from fullstack_token.base import AuthResponseHandlerBase
from services.auth_sqlalchemy import AuthServ
from fullstack_token.token import Token, AuthResponseHandlerToken

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login', auto_error=False)


def init_auth_res():
    auth_type = os.getenv('AUTH_TYPE')
    if auth_type == 'token':
        return AuthResponseHandlerToken()


def get_logged_in_user(_token: Token, service: AuthServ,
                       authorization: Annotated[Optional[str], Depends(oauth_scheme)] = None,
                       access_token_cookie: Annotated[Optional[str], Cookie()] = None):
    try:
        encoded = None
        if access_token_cookie is not None:
            encoded = access_token_cookie
        else:
            if authorization is not None:
                encoded = authorization
        if encoded is None:
            raise HTTPException(status_code=401, detail='unauthorized')

        validated = _token.validate(encoded)
        if validated['type'] != 'access':
            raise HTTPException(status_code=401, detail='Unauthorized')
        user = service.get_user_by_sub(validated['sub'])
        if user is None:
            raise HTTPException(status_code=401, detail='Unauthorized')

        return user
    except Exception as e:
        print('4')
        raise HTTPException(status_code=401, detail='Unauthorized')

LoggedInUser = Annotated[models.User, Depends(get_logged_in_user)]
AuthRes = Annotated[AuthResponseHandlerBase, Depends(init_auth_res)]

'''
class AuthRequiredHandlerToken(AuthRequiredHandlerBase):
    def verify(self, _token: Token, service: AuthServ,
               authorization: Annotated[Optional[str], Depends(oauth_scheme)] = None,
               access_token_cookie: Annotated[Optional[str], Cookie()] = None,
               _cookie: Annotated[Optional[SessionData], Depends(verifier)] = None):

        try:
            encoded = None
            if access_token_cookie is not None:
                encoded = access_token_cookie
            else:
                if authorization is not None:
                    encoded = authorization

            if encoded is None:
                raise HTTPException(status_code=401, detail='Unauthorized')
            validated = token.validate(encoded)
            if validated['type'] != 'access':
                raise HTTPException(status_code=401, detail='Unauthorized')

'''


