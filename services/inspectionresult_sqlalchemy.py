import dtos.inspectionresult
import models
from services.base_service import BaseService

class InspectionResultService(BaseService):
    def __init__(self, db: models.Db):
        super(InspectionResultService, self).__init__(db)

    def create(self, req: dtos.inspectionresult.CreateInspResReq, date, inpectionFormId):
        result = models.Inspectionresult(
            createdAt=date,
            value=req.value,
            note=req.note,
            title=req.title,
            inspectionform_id=inspectionFormId,
        )

        self.db.add(result)
        self.db.commit()

        return result

    # def get_all(self):
    #     environments = self.db.query(models.Environment).all()
    #     return environments
    #
    # def get_by_id(self, id:int):
    #     environment = self.db.query(models.Environment).filter(models.Environment.id == id).first()
    #     return environment
