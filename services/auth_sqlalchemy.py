from passlib.context import CryptContext

import dtos.auth
import models
from services.base_service import BaseService

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class AuthService(BaseService):
    def __init__(self, db: models.Db):
        super(AuthService, self).__init__(db)

    def register(self, req: dtos.auth.UserRegisterReq):
        user = models.User(
            lastName=req.firstName,
            firstName=req.firstName,
            email=req.username,
            password=bcrypt_context.hash(req.password),
            role='student'
        )

        self.db.add(user)
        self.db.commit()

        return user