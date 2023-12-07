from pydantic import BaseModel
from typing import List
from typing import Optional

class UserCreateReq(BaseModel):
    username: str
    password: str
    firstName: str
    lastName: str
    role: str

class UserCreateRes(BaseModel):
    username: str
    firstName: str
    lastName: str
    role: str

class UserUpdateReq(BaseModel):
    username: str
    firstName: str
    lastName: str
    role: str

class UserResItem(BaseModel):
    id: int
    username: str
    firstName: str
    lastName: str
    role: str

class UsersListRes(BaseModel):
    users: List[UserResItem]