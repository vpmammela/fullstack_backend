import dtos.inspectiontarget
import models
from services.base_service import BaseService

class InspectionTargetService(BaseService):
    def __init__(self, db: models.Db):
        super(InspectionTargetService, self).__init__(db)

    def create(self, req: dtos.inspectiontarget.CreateInspTargReq):
        inspectiontarget = models.Inspectiontarget(
            name=req.name,
            description=req.description,
            createdAt=req.createdAt,
            environment_id=req.environment_id,
            inspectiontargettype_id=req.inspectiontargettype_id
        )

        self.db.add(inspectiontarget)
        self.db.commit()

        return inspectiontarget

    def get_all(self):
        inspectiontargets = self.db.query(models.Inspectiontarget).all()
        return inspectiontargets

    def get_by_id(self, id:int):
        inspectiontarget = self.db.query(models.Inspectiontarget).filter(models.Inspectiontarget.id == id).first()
        return inspectiontarget

class InspectionTargetTypeService(BaseService):
    def __init__(self, db: models.Db):
        super(InspectionTargetTypeService, self).__init__(db)

    def create(self, req: dtos.inspectiontarget.CreateInspTargTypeReq):
        type = models.Inspectiontargettype(
            name=req.name
        )

        self.db.add(type)
        self.db.commit()

        return type

    def get_all(self):
        types = self.db.query(models.Inspectiontargettype).all()
        return types