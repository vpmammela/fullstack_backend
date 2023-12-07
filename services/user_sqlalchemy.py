import dtos.user
import models
from services.base_service import BaseService
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UserService(BaseService):
    def __init__(self, db: models.Db):
        super(UserService, self).__init__(db)

    def create(self, req: dtos.user.UserCreateReq):
        user = models.User(
            firstName=req.firstName,
            lastName=req.lastName,
            email=req.username,
            password=bcrypt_context.hash(req.password),
            role=req.role
        )

        self.db.add(user)
        self.db.commit()

        return user

    def get_all(self, role: str):
        if role == "admin":
            users = self.db.query(models.User).all()
        elif role == "staff":
            users = self.db.query(models.User).filter(models.User.role == "student").all()
        return users

    def get_by_id(self, id: int):
        user = self.db.query(models.User).filter(models.User.id == id).first()
        return user

    def update_user(self, id: int, req: dtos.user.UserUpdateReq):
        user = self.db.query(models.User).filter(models.User.id == id).first()
        if not user:
            raise ValueError(f"User with id {id} not found")

        user.firstName = req.firstName if req.firstName is not None else user.firstName
        user.lastName = req.lastName if req.lastName is not None else user.lastName
        user.email = req.username if req.username is not None else user.email
        user.role = req.role if req.role is not None else user.role
        self.db.commit()

        return user
