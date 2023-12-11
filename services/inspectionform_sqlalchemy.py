import dtos.inspectionform
import models
from services.base_service import BaseService
from sqlalchemy.orm import joinedload

class InspectionFormService(BaseService):
    def __init__(self, db: models.Db):
        super(InspectionFormService, self).__init__(db)

    def create(self, req: dtos.inspectionform.InspFormReq, createdAt, userId):

        inspectiontype = self.db.query(models.Inspectiontype).filter(models.Inspectiontype.name == req.inspectiontype).first()
        if inspectiontype is None:
            raise HTTPException(status_code=404, detail=f"Inspectiontype '{req.inspectiontype}' not found")

        form = models.Inspectionform(
            createdAt=createdAt,
            closedAt = None,
            user_id = userId,
            environment_id = req.environment_id,
            inspectiontarget_id = req.inspectiontarget_id,
            inspectiontype_id = inspectiontype.id
        )

        self.db.add(form)
        self.db.commit()

        return form

    def get_by_id(self, id: int):
        return self.db.query(models.Inspectionform). \
            options(joinedload(models.Inspectionform.files)). \
            filter(models.Inspectionform.id == id).all()
