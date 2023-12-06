from fastapi import APIRouter, Depends
from starlette.responses import Response
from fastapi.security import OAuth2PasswordRequestForm
from fullstack_token.session import backend, cookie, verifier
from fastapi import Depends, HTTPException
from pydantic import BaseModel
from typing import Annotated
import models
from dtos.inspectionform import InspFormRespItem, InspFormReq
from services.inspectionform_sqlalchemy import InspectionFormService
from services.auth_sqlalchemy import AuthService, AuthServ
from dependencies import LoggedInUser
from datetime import datetime


router = APIRouter(
    tags=['inspectionform'],
    prefix='/api/v1'
)

LoginForm = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/inspectionform', dependencies=[Depends(cookie)], response_model=InspFormRespItem)
async def create(req: InspFormReq, authService: AuthServ, account: LoggedInUser, service: InspectionFormService = Depends(InspectionFormService)):
    createdAt = datetime.now()
    userId = account.id
    form = service.create(req, createdAt, userId)
    return InspFormRespItem(id=form.id, environment_id=form.environment_id, inspectiontarget_id=form.inspectiontarget_id, inspectiontype_id=form.inspectiontype_id)
