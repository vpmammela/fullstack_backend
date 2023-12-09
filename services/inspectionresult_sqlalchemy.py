"""import dtos.inspectionresult
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
        """
    
import dtos.inspectionresult
import models
from services.base_service import BaseService
from typing import List

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

    def get_inspection_results_by_form_id(self, inspection_form_id: int) -> List[models.Inspectionresult]:
        return self.db.query(models.Inspectionresult).filter_by(inspectionform_id=inspection_form_id).all()
