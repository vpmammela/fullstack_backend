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
    reports_resp_list = service.generate_reports_resp_list(reports)

    return InspectionresultListResponse(items=reports_resp_list)

@router.get('/report/inspectiontarget/{id}/{inspectionType}', dependencies=[Depends(cookie)], response_model=InspectionresultListResponse)
async def get_report_by_inspectiontarget_id_and_inspection_type(id: int, inspectionType: str, account: LoggedInUser, service: ReportService = Depends(ReportService)):
    reports = service.get_by_inspectiontarget_id(id, inspectionType)
    reports_resp_list = service.generate_reports_resp_list(reports)

    return InspectionresultListResponse(items=reports_resp_list)

@router.get('/report/{inspectionType}', dependencies=[Depends(cookie)], response_model=InspectionresultListResponse)
async def get_report_by_inspectiontype(inspectionType: str, account: LoggedInUser, service: ReportService = Depends(ReportService)):
    reports = service.get_by_inspectiontype(inspectionType)
    reports_resp_list = service.generate_reports_resp_list(reports)

    return InspectionresultListResponse(items=reports_resp_list)
