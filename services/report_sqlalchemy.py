import dtos.report
import models
from services.base_service import BaseService
from sqlalchemy.orm import joinedload

class ReportService(BaseService):
    def __init__(self, db: models.Db):
        super(ReportService, self).__init__(db)

    def get_by_environment_id(self, id: int, inspectionType: str):
        inspection_results = (
            self.db.query(models.Inspectionresult)
                .join(models.Inspectionform)
                .join(models.Environment)
                .join(models.Inspectiontype)
                .filter(
                models.Environment.id == id,
                models.Inspectiontype.name == inspectionType
            )
                .options(joinedload(models.Inspectionresult.inspectionform))
                .all()
        )

        return inspection_results

    def get_by_inspectiontarget_id(self, id: int, inspectionType: str):
        inspection_results = (
            self.db.query(models.Inspectionresult)
                .join(models.Inspectionform)
                .join(models.Inspectiontarget)
                .join(models.Inspectiontype)
                .filter(
                models.Inspectiontarget.id == id,
                models.Inspectiontype.name == inspectionType
            )
                .options(joinedload(models.Inspectionresult.inspectionform))
                .all()
        )

        return inspection_results

    def get_by_inspectiontype(self, inspectionType: str):
        inspection_results = (
            self.db.query(models.Inspectionresult)
                .join(models.Inspectionform)
                .join(models.Inspectiontype)
                .filter(models.Inspectiontype.name == inspectionType)
                .options(joinedload(models.Inspectionresult.inspectionform))
                .all()
        )

        return inspection_results

    def generate_reports_resp_list(self, reports):
        return [
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
