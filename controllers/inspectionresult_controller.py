from fastapi import APIRouter, Depends
from starlette.responses import Response
from fastapi.security import OAuth2PasswordRequestForm
from fullstack_token.session import backend, cookie, verifier
from fastapi import Depends, HTTPException
from pydantic import BaseModel
from typing import Annotated
import models
from dtos.inspectionresult import InspResResp, CreateInspResReq
from services.inspectionresult_sqlalchemy import InspectionResultService
from services.auth_sqlalchemy import AuthService, AuthServ
from dependencies import LoggedInUser
from datetime import datetime


router = APIRouter(
    tags=['inspectionresult'],
    prefix='/api/v1'
)

LoginForm = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/inspectionresult', dependencies=[Depends(cookie)], response_model=InspResResp)
async def create_inspection_result(req: CreateInspResReq, authService: AuthServ, account: LoggedInUser, service: InspectionResultService = Depends(InspectionResultService)):
    createdAt = datetime.now()
    inspectionresult = service.create(req, createdAt)
    return InspResResp(id=inspectionresult.id, title=inspectionresult.title, note=inspectionresult.note)
