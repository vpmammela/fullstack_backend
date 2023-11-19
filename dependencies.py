import os
from typing import Optional, Annotated
from dtos.auth import SessionData

from fastapi import Depends, Cookie, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fullstack_token.session import AuthResponseHandlerSession

import models
from fullstack_token.base import AuthResponseHandlerBase
from services.auth_sqlalchemy import AuthServ
from fullstack_token.token import Token, AuthResponseHandlerToken
from fullstack_token.session import verifier

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login', auto_error=False)

class AuthRequiredHandlerBase:
    def verify(self, _token: Token, service: AuthServ,
                authorization: Annotated[Optional[str], Depends(oauth_scheme)] = None,
                access_token_cookie: Annotated[Optional[str], Cookie()] = None,
                _cookie: Annotated[Optional[SessionData], Depends(verifier)] = None):
        pass
    
class AuthRequiredHandleToken(AuthRequiredHandlerBase):
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
                raise HTTPException(status_code=401, detail='unauthorized Token 1')

            validated = _token.validate(encoded)
            if validated['type'] != 'access':
                raise HTTPException(status_code=401, detail='Unauthorized Token 2')
            user = service.get_user_by_sub(validated['sub'])
            if user is None:
                raise HTTPException(status_code=401, detail='Unauthorized Token 3')

            return user
        except Exception as e:
            print('4')
            raise HTTPException(status_code=401, detail='Unauthorized Token 4')

class AuthRequiredHandlerSession(AuthRequiredHandlerBase):
    def verify(self, _token: Token, service: AuthServ,
               authorization: Annotated[Optional[str], Depends(oauth_scheme)] = None,
               access_token_cookie: Annotated[Optional[str], Cookie()] = None,
               _cookie: Annotated[Optional[SessionData], Depends(verifier)] = None):
    
        try:
            if _cookie is None:
                raise HTTPException(status_code=401, detail='Unauthorized1')
            
            user = service.get_user_by_sub(_cookie.data)
            
            if user is None:
                raise HTTPException(status_code=401, detail='Unauthorized2')
            return user
        except Exception as e:
            raise HTTPException(status_code=401, detail='Unauthorized3')
            
            

def init_auth_res():
    auth_type = os.getenv('AUTH_TYPE')
    if auth_type == 'session':
        return AuthResponseHandlerSession()
    else:
        return AuthResponseHandlerToken()
    
def init_auth_handler():
    auth_type = os.getenv('AUTH_TYPE')
    if auth_type == 'session':
        return AuthRequiredHandlerSession()
    else:
        return AuthRequiredHandleToken()
    
AccountHandler = Annotated[AuthRequiredHandlerBase, Depends(init_auth_handler)]


def get_logged_in_user(_token: Token, service: AuthServ, account_handler: AccountHandler,
                       authorization: Annotated[Optional[str], Depends(oauth_scheme)] = None,
                       access_token_cookie: Annotated[Optional[str], Cookie()] = None,
                       _cookie: Annotated[Optional[SessionData], Depends(verifier)] = None):

    return account_handler.verify(_token, service, authorization, access_token_cookie, _cookie)
    
    


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


