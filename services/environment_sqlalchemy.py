import dtos.environment
import models
from services.base_service import BaseService

class EnvironmentService(BaseService):
    def __init__(self, db: models.Db):
        super(EnvironmentService, self).__init__(db)

    def create(self, req: dtos.environment.CreateEnvReq):
        environment = models.Environment(
            name=req.name,
            description=req.description,
            location_id=req.location_id,
            environmenttype_id=req.environmenttype_id,
        )

        self.db.add(environment)
        self.db.commit()

        return environment

    def get_all(self):
        environments = self.db.query(models.Environment).all()
        return environments

    def get_by_id(self, id:int):
        environment = self.db.query(models.Environment).filter(models.Environment.id == id).first()
        return environment

class EnvironmentTypeService(BaseService):
    def __init__(self, db: models.Db):
        super(EnvironmentTypeService, self).__init__(db)

    def create(self, req: dtos.environment.CreateEnvTypeReq):
        type = models.Environmenttype(
            name=req.name
        )

        self.db.add(type)
        self.db.commit()

        return type

    def get_all(self):
        types = self.db.query(models.Environmenttype).all()
        return types