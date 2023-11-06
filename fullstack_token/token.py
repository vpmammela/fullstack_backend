import os
import time
from typing import Annotated

import jwt
from fastapi import Depends


class BaseToken:
    def create(self, claims):
        pass

    def validate(self, t):
        pass


class SymmetricToken(BaseToken):
    secret = os.getenv('JWT_SECRET')

    def create(self, claims):
        secret = os.getenv('JWT_SECRET')
        now = time.time()
        issuer = 'fullstackmvp'
        audience = 'localhost'
        _type = claims['type']
        exp = claims['exp']
        sub = claims['sub']

        data = {'iss': issuer, 'aud': audience, 'type': _type, 'sub': sub, 'iat': now, 'nbf': now - 10}
        if exp is not None:
            data['exp'] = exp

        _token = jwt.encode(data, secret, algorithm='HS512')
        return _token


class AsymmetricToken(BaseToken):
    def __init__(self):
        with open('cert/id_rsa') as f:
            self.private = f.read()
        with open('cert/id_rsa.pub') as f:
            self.public = f.read()

    def create(self, claims):
        now = time.time()
        issuer = 'fullstackmvp'
        audience = 'localhost'
        _type = claims['type']
        exp = claims['exp']
        sub = claims['sub']
        csrf = claims['csrf']

        data = {'iss': issuer, 'aud': audience, 'type': _type, 'sub': sub, 'iat': now, 'nbf': now - 10}
        if exp is not None:
            data['exp'] = exp
        if csrf is not None:
            data['csrf'] = csrf

        _token = jwt.encode(data, self.private, algorithm='RS512')
        return _token

    def validate(self, t):
        claims = jwt.decode(t, self.public, algorithms=['RS512'], audience='localhost')
        return claims

def init_token():
    _type = os.getenv('JWT_TYPE')
    if _type == 'symmetric':
        return SymmetricToken()
    elif _type == 'asymmetric':
        return AsymmetricToken()


Token = Annotated[BaseToken, Depends(init_token)]
