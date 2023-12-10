from fastapi import APIRouter, Depends
from starlette.responses import Response
from fastapi.security import OAuth2PasswordRequestForm
from fullstack_token.session import backend, cookie, verifier
from fastapi import Depends, HTTPException
from pydantic import BaseModel
from typing import Annotated
import models
from dtos.report import InspectionresultListResponse
from services.report_sqlalchemy import ReportService
from services.auth_sqlalchemy import AuthService, AuthServ
from dependencies import LoggedInUser


router = APIRouter(
    tags=['report'],
    prefix='/api/v1'
)

LoginForm = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.get('/report/environment/{id}/{inspectionType}', dependencies=[Depends(cookie)], response_model=InspectionresultListResponse)
async def get_report_by_environment_id_and_inspection_type(id: int, inspectionType: str, account: LoggedInUser, service: ReportService = Depends(ReportService)):
    reports = service.get_by_environment_id(id, inspectionType)
    users_resp_list = [
        {
            "id": result.id,
            "note": result.note,
            "inspectionform_id": result.inspectionform_id,
            "createdAt": result.createdAt.isoformat(),
            "value": result.value,
            "title": result.title,
            "inspectionform": {
                "createdAt": result.inspectionform.createdAt.isoformat(),
                "user_id": result.inspectionform.user_id,
                "inspectiontarget_id": result.inspectionform.inspectiontarget_id,
                "id": result.inspectionform.id,
                "closedAt": result.inspectionform.closedAt.isoformat() if result.inspectionform.closedAt else None,
                "environment_id": result.inspectionform.environment_id,
                "inspectiontype_id": result.inspectionform.inspectiontype_id
            }
        }
        for result in reports
    ]

    return InspectionresultListResponse(reports=users_resp_list)


