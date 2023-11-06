import time
import uuid
from typing import Annotated

from passlib.context import CryptContext

import dtos.auth
import models
from fullstack_token.token import BaseToken, Token
from services.base_service import BaseService
from fastapi import Depends

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class AuthService(BaseService):
    def __init__(self, db: models.Db):
        super(AuthService, self).__init__(db)

    def register(self, req: dtos.auth.UserRegisterReq):
        user = models.User(
            firstName=req.firstName,
            lastName=req.lastName,
            email=req.username,
            password=bcrypt_context.hash(req.password),
            role='student'
        )

        self.db.add(user)
        self.db.commit()

        return user

    def get_user_by_sub(self, sub):
        user = self.db.query(models.User).filter(models.User.access_token_identifier == sub).first()
        return user

    def login(self, username: str, password: str, csrf: str, _token: Token):
        user = self.db.query(models.User).filter(models.User.email == username).first()
        if user is None:
            return None, None
        valid = bcrypt_context.verify(password, user.password)
        if not valid:
            return None, None

        now = time.time()
        access_token_sub = str(uuid.uuid4())
        refresh_token_sub = str(uuid.uuid4())
        access_token = _token.create({'type': 'access', 'sub': access_token_sub, 'exp': now + 3600, 'csrf': csrf})
        refresh_token = _token.create({'type': 'refresh', 'sub': refresh_token_sub, 'exp': now + 3600*24, 'csrf': None})
        csrf_token = _token.create({'type': 'csrf', 'sub': csrf, 'exp': None, 'csrf': None})

        user.access_token_identifier = access_token_sub
        user.refresh_token_identifier = refresh_token_sub
        self.db.commit()

        return access_token, refresh_token, csrf_token
def get_auth_service(db: models.Db):
    return AuthService(db)

AuthServ = Annotated[AuthService, Depends(get_auth_service)]