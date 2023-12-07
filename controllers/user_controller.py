from fastapi import APIRouter, Depends
from starlette.responses import Response
from fastapi.security import OAuth2PasswordRequestForm
from fullstack_token.session import backend, cookie, verifier
from fastapi import Depends, HTTPException
from pydantic import BaseModel
from typing import Annotated
import models
from dtos.user import UserCreateRes, UserCreateReq, UsersListRes, UserResItem, UserUpdateReq
from services.user_sqlalchemy import UserService
from services.auth_sqlalchemy import AuthService, AuthServ
from dependencies import LoggedInUser

router = APIRouter(
    tags=['user'],
    prefix='/api/v1'
)

LoginForm = Annotated[OAuth2PasswordRequestForm, Depends()]

@router.post('/user', dependencies=[Depends(cookie)], response_model=UserCreateRes)
async def create_new_user(req: UserCreateReq, authService: AuthServ, account: LoggedInUser, service: UserService = Depends(UserService)):
    if account.role != "admin":
        raise HTTPException(status_code=401, detail='unauthorized')
    else:
        user = service.create(req)
        return UserCreateRes(username=user.email, firstName=user.firstName, lastName=user.lastName, role=user.role)

@router.get('/user/{id}', dependencies=[Depends(cookie)], response_model=UserResItem)
async def get_user_by_id(id:int, authService: AuthServ, account: LoggedInUser, service: UserService = Depends(UserService)):
    if account.role != "admin":
        raise HTTPException(status_code=401, detail='unauthorized')
    else:
        user = service.get_by_id(id)
        return UserResItem(id=user.id, username=user.email, firstName=user.firstName, lastName=user.lastName, role=user.role)

@router.put('/user/{id}', dependencies=[Depends(cookie)], response_model=UserResItem)
async def update_user(id: int, req: UserUpdateReq, authService: AuthServ, account: LoggedInUser, service: UserService = Depends(UserService)):
    if account.role != "admin":
        raise HTTPException(status_code=401, detail='unauthorized')
    else:
        updated_user = service.update_user(id, req)
        return UserResItem(id=updated_user.id, username=updated_user.email, firstName=updated_user.firstName, lastName=updated_user.lastName, role=updated_user.role)

@router.get('/users', dependencies=[Depends(cookie)], response_model=UsersListRes)
async def get_all_users(authService: AuthServ, account: LoggedInUser, service: UserService = Depends(UserService)):
    if account.role == "student":
        raise HTTPException(status_code=401, detail='unauthorized')
    else:
        users = service.get_all(account.role)
        users_resp_list = [{"id": user.id, "username": user.email, "firstName": user.firstName, "lastName": user.lastName, "role": user.role} for user in users]
        return UsersListRes(users=users_resp_list)

