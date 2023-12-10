from fastapi import APIRouter, Depends, UploadFile
from starlette.responses import Response
from fastapi.security import OAuth2PasswordRequestForm
from fullstack_token.session import backend, cookie, verifier
from fastapi import Depends, HTTPException, UploadFile
from pydantic import BaseModel
from typing import Annotated
import models
import uuid
from dtos.inspectionform import InspFormRespItem, InspFormReq
from services.inspectionform_sqlalchemy import InspectionFormService
from services.auth_sqlalchemy import AuthService, AuthServ
from services.file_service import FileService
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
    createdAt = createdAt.strftime('%Y-%m-%d %H:%M:%S')
    userId = account.id
    form = service.create(req, createdAt, userId)
    return InspFormRespItem(id=form.id, environment_id=form.environment_id, inspectiontarget_id=form.inspectiontarget_id, inspectiontype_id=form.inspectiontype_id)


# For photos in forms. 
@router.post("/inspectionform/{id}/image", dependencies=[Depends(cookie)])
async def upload_image(id: int, image: UploadFile):
    try:
        random_name = str(uuid.uuid4()) + '.png'
        file_path = f'static/images/{random_name}'

        with open(file_path, 'wb') as file:
            file.write(await image.read())

        return {"message": "Image uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get('/inspectionform/{id}', dependencies=[Depends(cookie)], response_model=InspFormRespItem)
async def get_form(id: int, service: InspectionFormService = Depends(InspectionFormService)):
    form = service.get_by_id(id)
    if form is None:
        raise HHTPException(statues_code=404, detaisl='not found')
    return InspFormRespItem(id=form.id, environment_id=form.environment_id, inspectiontarget_id=form.inspectiontarget_id, inspectiontype_id=form.inspectiontype_id)