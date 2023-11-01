from pydantic import BaseModel


class UserRegisterReq(BaseModel):
    username: str
    password: str
    firstName: str
    lastName: str


class UserRegisterRes(BaseModel):
    username: str
    firstName: str
    lastName: str


class UserLoginRes(BaseModel):
    access_token: str
    refresh_token: str
