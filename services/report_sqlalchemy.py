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