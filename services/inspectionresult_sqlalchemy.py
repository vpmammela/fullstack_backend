import dtos.inspectionresult
import models
from services.base_service import BaseService

class InspectionResultService(BaseService):
    def __init__(self, db: models.Db):
        super(InspectionResultService, self).__init__(db)

    def create(self, req: dtos.inspectionresult.CreateInspResReq, createdAt):
        result = models.Inspectionresult(
            createdAt=createdAt,
            value=req.value,
            note=req.note,
            title=req.title,
            inspectionform_id=req.inspectionform_id,
        )

        self.db.add(result)
        self.db.commit()

        return result
