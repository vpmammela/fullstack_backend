from fastapi import APIRouter, Depends, UploadFile
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
    createdAt = createdAt.strftime('%Y-%m-%d %H:%M:%S')
    userId = account.id
    form = service.create(req, createdAt, userId)
    return InspFormRespItem(id=form.id, environment_id=form.environment_id, inspectiontarget_id=form.inspectiontarget_id, inspectiontype_id=form.inspectiontype_id)


# For photos in forms. 
@router.post("/{form_id/image")
async def upload_image(form_id: int, image: UploadFile, file_service: FileService):
    random_name = str(uuid.uuid4())
    random_name += '.png'
    with open(f'static/images/{random_name}', 'wb') as file:
        file.write(await image.read())
        file_service.upload(form_id, original_name=image.filename, random_name=random_name)
    return True

@router.get('/{form_id}')
async def get_form(form_id: int, service: FormSErvice):
    form = service.get_by_id(form_id)
    if form is None:
        raise HHTPException(statues_code=404, detaisl='not found')
    return {'form: form'}